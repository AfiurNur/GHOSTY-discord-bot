import discord
from discord import app_commands
from discord.ext import commands
import requests
guild_id = 1242396018704908289

class hololive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.lunardev.group"  # Base URL for the LunarDev API
        self.nsfw_hololive_endpoint = "/nsfw/hololive"  # NSFW hololive endpoint


    def fetch_nsfw_hololive_image(self):
        try:
            response = requests.get(f'{self.base_url}{self.nsfw_hololive_endpoint}')
            if response.status_code == 200:
                data = response.json()

                image_url = data.get('url', None)
                if image_url:
                    return image_url
                else:
                    print(f"Error: No 'url' field in response data. Response: {data}")
                    return None
            else:
                print(f"Error fetching image: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f'Error: {str(e)}')
            return None
        

    @app_commands.command(name="nsfw_hololive", description="Fetches an NSFW hololive image")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def nsfw_hololive(self, interaction: discord.Integration):
        image_url = self.fetch_nsfw_hololive_image()

        if interaction.channel and interaction.channel.nsfw:

            if image_url:
                embed = discord.Embed(
                    title="NSFW Hololive Image",
                    description="Here is your requested NSFW hololive image!",
                    color=discord.Color.blurple()
                )
                embed.set_image(url=image_url)
                await interaction.response.send_message(embed=embed)
            else:
                # If there was no image, send an error message to the user
                await interaction.response.send_message("Could not fetch the image. Please try again later.")
        else:
            await interaction.response.send_message("This command can only be used in NSFW channels.", ephemeral=True)


# Set up the cog
async def setup(bot):
    await bot.add_cog(hololive(bot))