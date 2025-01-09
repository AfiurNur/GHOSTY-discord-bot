import discord
from discord import app_commands
from discord.ext import commands
import requests
guild_id = 1242396018704908289
class Ahegao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.lunardev.group"  # Base URL for the LunarDev API
        self.nsfw_ahegao_endpoint = "/nsfw/ahegao"  # NSFW ahegao endpoint

    # Function to fetch the image from the LunarDev API
    def fetch_nsfw_ahegao_image(self):
        """Fetch an NSFW ahegao image from LunarDev API."""
        try:
            # Send a request to the API
            response = requests.get(f"{self.base_url}{self.nsfw_ahegao_endpoint}")

            # Check if the status code is 200 (OK)
            if response.status_code == 200:
                data = response.json()
                
                # Now using the 'url' field to get the image
                image_url = data.get('url', None)
                
                if image_url:
                    return image_url
                else:
                    print(f"Error: No 'url' field in response data. Response: {data}")
                    return None
            else:
                # If the response status code is not 200, log the error
                print(f"Error fetching image: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            # Catch any exceptions and log the error
            print(f"Error: {str(e)}")
            return None

    # Slash command to fetch the NSFW ahegao image and send it in the Discord channel
    @app_commands.command(name="nsfw_ahegao", description="Fetches an NSFW ahegao image from LunarDev API.")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def nsfw_ahegao(self, interaction: discord.Interaction):
        """Fetch and send NSFW ahegao image to the Discord channel."""
        image_url = self.fetch_nsfw_ahegao_image()

        if interaction.channel and interaction.channel.nsfw:

            if image_url:
                embed = discord.Embed(
                    title="NSFW Ahegao Image",
                    description="Here is your requested NSFW ahegao image!",
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
    await bot.add_cog(Ahegao(bot))
