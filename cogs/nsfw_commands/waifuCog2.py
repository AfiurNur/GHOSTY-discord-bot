import discord
from discord.ext import commands
from discord import app_commands
import nekos
import random

guild_id = 1242396018704908289  # Replace with your guild ID

class NekoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Function to fetch an image based on the tag using nekos.img()
    async def fetch_neko_image(self, tag: str):
        """Dynamically fetch image based on the selected tag."""
        # Use nekos.img() for fetching images
        try:
            return nekos.img(tag)
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None

    # Command to fetch an image based on the tag
    @app_commands.command(name="neko_image", description="Get a neko image based on the specified tag!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def neko_image(self, interaction: discord.Interaction, tag: str):
        """Fetch an image based on the tag provided by the user."""
        await interaction.response.defer()  # Defer the interaction response to buy time

        # Fetch the image
        image_url = await self.fetch_neko_image(tag)

        if not image_url:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Invalid Tag!",
                    description=f"The tag `{tag}` is not valid. Use `/neko_tags` to see available tags.",
                    color=discord.Color.red(),
                )
            )
            return

        # Create embed to display image
        embed = discord.Embed(
            title=f"Here's your {tag} image!",
            color=discord.Color.blurple()
        )
        embed.set_image(url=image_url)

        await interaction.followup.send(embed=embed)

    # Command to show the available neko tags
    @app_commands.command(name="neko_tags", description="Get all available neko tags!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def neko_tags(self, interaction: discord.Interaction):
        """Show the available neko tags to the user."""
        await interaction.response.defer()  # Defer the interaction response to buy time

        # Tags available for the user (as defined in nekos library)
        tags = ["wallpaper", "ngif", "tickle", "feed", "gecg", "gasm", "slap", "avatar", "lizard", "waifu", "pat", "8ball", "kiss", "neko", "spank", "cuddle", "fox_girl", "hug", "smug", "goose", "woof"]

        embed = discord.Embed(
            title="Available Neko Tags",
            description=", ".join(tags),
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

    # Command to fetch a random neko image using img()
    @app_commands.command(name="random_neko", description="Get a random neko image!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def random_neko(self, interaction: discord.Interaction):
        """Fetch a random image from one of the available tags using nekos.img()"""
        await interaction.response.defer()  # Defer the interaction response to buy time

        # Available tags for random neko
        available_tags = ["wallpaper", "ngif", "tickle", "feed", "gecg", "gasm", "slap", "avatar", "lizard", "waifu", "pat", "8ball", "kiss", "neko", "spank", "cuddle", "fox_girl", "hug", "smug", "goose", "woof"]

        # Randomly select a tag
        tag = random.choice(available_tags)
        image_url = await self.fetch_neko_image(tag)

        if not image_url:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Error!",
                    description="Could not fetch a random image. Please try again later.",
                    color=discord.Color.red(),
                )
            )
            return

        # Create embed for the random image
        embed = discord.Embed(
            title=f"Here's a random {tag} image for you!",
            color=discord.Color.blurple()
        )
        embed.set_image(url=image_url)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NekoCog(bot))
