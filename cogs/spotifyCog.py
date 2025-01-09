import discord
from discord import app_commands
from discord.ext import commands

guild_id = 1242396018704908289

class SpotifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="spotify", description="Get Spotify activity of a user")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def spotify(self, interaction: discord.Interaction, member: discord.Member = None):
        """
        Fetch Spotify activity for a member
        """
        member = member or interaction.user  # Default to the command issuer if no member is provided

        # Check if the member has Spotify activity
        spotify_activity = next(
            (activity for activity in member.activities if isinstance(activity, discord.Spotify)), 
            None
        )

        if not spotify_activity:
            await interaction.response.send_message(f"{member.display_name} is not currently listening to Spotify.", ephemeral=True)
            return

        # Create an embed with Spotify details
        embed = discord.Embed(
            title=f"{member.display_name}'s Spotify Activity",
            description=f"**Track:** {spotify_activity.name}\n"
                        f"**Artist(s):** {', '.join(spotify_activity.artists)}\n"
                        f"**Album:** {spotify_activity.album}",
            color=spotify_activity.color
        )
        embed.set_author(name="Afiur nur", icon_url="https://media.discordapp.net/attachments/898426430537469963/1323306705916002395/wallhaven-v99yvm.jpg?ex=677408e8&is=6772b768&hm=1d1b3b7b4ca975ab192d19c017d645755adf2ca0f9401bf01931f81acc515885&=&format=webp&width=882&height=496")
        embed.set_thumbnail(url=spotify_activity.album_cover_url)
        embed.add_field(
            name="Track Link",
            value=f"[Listen on Spotify](https://open.spotify.com/track/{spotify_activity.track_id})",
            inline=False
        )
        embed.set_footer(
            text=f"Started at: {spotify_activity.start.strftime('%H:%M:%S')} | Ends at: {spotify_activity.end.strftime('%H:%M:%S')}",
        )

        # Respond with the embed
        await interaction.response.send_message(embed=embed)

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(SpotifyCog(bot))
