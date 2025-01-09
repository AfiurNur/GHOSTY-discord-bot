import discord
from discord import app_commands
from discord.ext import commands
import requests
guild_id = 1242396018704908289

class Neko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.lunardev.group"  # Base URL for the LunarDev API
        self.nsfw_neko_endpoint = "/nsfw/neko"  # NSFW neko endpoint

    def fetch_nsfw_neko_image(self):
        try:
            response = requests.get(f'{self.base_url}{self.nsfw_neko_endpoint}')
            
            # Check if response is not empty and status code is 200
            if response.status_code == 200:
                # Ensure the response is valid JSON
                try:
                    data = response.json()
                    image_url = data.get('url', None)

                    if image_url:
                        return image_url
                    else:
                        print(f"Error: 'url' not found in response. Response: {data}")
                        return None
                except ValueError:
                    print("Error: Response is not a valid JSON.")
                    return None
            else:
                print(f"Error fetching image: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f'Error: {str(e)}')
            return None

    @app_commands.command(name="nsfw_neko", description="Fetches an NSFW neko image")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def nsfw_neko(self, interaction: discord.Interaction):
        image_url = self.fetch_nsfw_neko_image()

        if interaction.channel and interaction.channel.nsfw:

            if image_url:
                embed = discord.Embed(
                    title="NSFW neko Image",
                    description="Here is your requested NSFW neko image!",
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
    await bot.add_cog(Neko(bot))
