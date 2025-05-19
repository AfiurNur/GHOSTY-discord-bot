import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio

GUILD_ID = 1242396018704908289  # Replace with your actual guild ID


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.voice_clients = {}
        self.yt_dl_options = {"format": "bestaudio/best"}
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -filter:a "volume=0.25"'
        }

    def play_next(self, guild_id):
        if guild_id in self.queues and self.queues[guild_id]:
            next_song = self.queues[guild_id].pop(0)
            voice_client = self.voice_clients[guild_id]
            player = discord.FFmpegOpusAudio(next_song['url'], **self.ffmpeg_options)
            voice_client.play(player, after=lambda e: self.play_next(guild_id))

    async def ensure_voice_connection(self, interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("You need to be in a voice channel to use this command.", ephemeral=True)
            return False

        if interaction.guild.id not in self.voice_clients or not self.voice_clients[interaction.guild.id].is_connected():
            voice_client = await interaction.user.voice.channel.connect()
            self.voice_clients[interaction.guild.id] = voice_client

        return True

    @app_commands.command(name="play", description="Play a song, YouTube/Spotify URL, or search query.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def play(self, interaction: discord.Interaction, query: str):
        if not await self.ensure_voice_connection(interaction):
            return

        await interaction.response.defer()
        guild_id = interaction.guild.id
        self.queues.setdefault(guild_id, [])
        songs = []

        try:
            if "spotify.com" in query:
                info = await asyncio.to_thread(lambda: self.ytdl.extract_info(query, download=False))

                # If it's a playlist
                if "entries" in info:
                    for entry in info["entries"]:
                        title = entry.get("track") or entry.get("title")
                        artist = entry.get("artist", "")
                        search_query = f"{title} {artist}".strip()
                        yt_data = await asyncio.to_thread(lambda: self.ytdl.extract_info(f"ytsearch:{search_query}", download=False))
                        if yt_data and "entries" in yt_data and yt_data["entries"]:
                            video = yt_data["entries"][0]
                            songs.append({
                                "title": video["title"],
                                "url": video["url"],
                                "webpage_url": video.get("webpage_url"),
                                "thumbnail": video.get("thumbnail")
                            })

                else:  # Single track
                    title = info.get("track") or info.get("title")
                    artist = info.get("artist", "")
                    search_query = f"{title} {artist}".strip()
                    yt_data = await asyncio.to_thread(lambda: self.ytdl.extract_info(f"ytsearch:{search_query}", download=False))
                    if yt_data and "entries" in yt_data and yt_data["entries"]:
                        video = yt_data["entries"][0]
                        songs.append({
                            "title": video["title"],
                            "url": video["url"],
                            "webpage_url": video.get("webpage_url"),
                            "thumbnail": video.get("thumbnail")
                        })

            else:
                # YouTube direct link or search
                yt_data = await asyncio.to_thread(lambda: self.ytdl.extract_info(query, download=False))
                if "entries" in yt_data:
                    yt_data = yt_data["entries"][0]
                songs.append({
                    "title": yt_data["title"],
                    "url": yt_data["url"],
                    "webpage_url": yt_data.get("webpage_url"),
                    "thumbnail": yt_data.get("thumbnail")
                })

            self.queues[guild_id].extend(songs)
            vc = self.voice_clients[guild_id]
            if not vc.is_playing() and not vc.is_paused():
                self.play_next(guild_id)

            if len(songs) > 1:
                await interaction.followup.send(f"✅ Added **{len(songs)} tracks** from playlist to the queue.")
            else:
                song = songs[0]
                embed = discord.Embed(
                    title="Added to Queue" if vc.is_playing() else "Now Playing",
                    description=f"**[{song['title']}]({song['webpage_url']})**",
                    color=discord.Color.blurple()
                )
                if song["thumbnail"]:
                    embed.set_thumbnail(url=song["thumbnail"])
                embed.set_footer(text="GHOSTY - Multipurpose bot by Afiur Nur")
                await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error: {e}")

    @app_commands.command(name="pause", description="Pause the currently playing song.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def pause(self, interaction: discord.Interaction):
        voice_client = self.voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("⏸️ Playback paused.")
        else:
            await interaction.response.send_message("No song is currently playing.")

    @app_commands.command(name="resume", description="Resume the paused song.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def resume(self, interaction: discord.Interaction):
        voice_client = self.voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("▶️ Playback resumed.")
        else:
            await interaction.response.send_message("No song is currently paused.")

    @app_commands.command(name="skip", description="Skip the current song.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def skip(self, interaction: discord.Interaction):
        voice_client = self.voice_clients.get(interaction.guild.id)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ Skipped the current song.")
        else:
            await interaction.response.send_message("No song is currently playing.")

    @app_commands.command(name="queue", description="View the current song queue.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def queue(self, interaction: discord.Interaction):
        if interaction.guild.id not in self.queues or not self.queues[interaction.guild.id]:
            await interaction.response.send_message("The queue is currently empty.")
            return

        queue_list = "\n".join([f"{idx + 1}. {song['title']}" for idx, song in enumerate(self.queues[interaction.guild.id])])
        embed = discord.Embed(
            title="🎶 Current Queue",
            description=queue_list,
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stop", description="Stop playback and disconnect the bot.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def stop(self, interaction: discord.Interaction):
        voice_client = self.voice_clients.get(interaction.guild.id)
        if voice_client:
            voice_client.stop()
            await voice_client.disconnect()
            del self.voice_clients[interaction.guild.id]
            self.queues.pop(interaction.guild.id, None)
            await interaction.response.send_message("⏹️ Playback stopped and disconnected.")
        else:
            await interaction.response.send_message("The bot is not connected to a voice channel.")


# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(MusicCog(bot))
