import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from waifuim import WaifuAioClient
import random
import aiohttp

guild_id = 1242396018704908289

class WaifuCog1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = WaifuAioClient()
        self.tags = {}

    async def fetch_tags(self):
        """Fetch and cache all available tags, categorized as SFW and NSFW."""
        try:
            print("Fetching tags...")
            url = 'https://api.waifu.im/tags'  # Correct URL for fetching tags
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"Raw response data: {data}")  # Log the raw response data
                        # Categorize tags into 'sfw' and 'nsfw'
                        self.tags = {
                            "SFW": data.get('versatile', []),  # SFW tags
                            "NSFW": data.get('nsfw', []),  # NSFW tags
                        }
                        print(f"Tags fetched: SFW - {len(self.tags['SFW'])}, NSFW - {len(self.tags['NSFW'])}")
                    else:
                        print(f"Failed to fetch tags. Status code: {response.status}")
        except Exception as e:
            print(f"Error fetching tags: {e}")
            self.tags = {"SFW": [], "NSFW": []}

    async def fetch_image(self, included_tags: list = None, excluded_tags: list = None, height: str = None):
        """Fetch a waifu image using search API."""
        try:
            print(f"Fetching image with tags: {included_tags}, excluded_tags: {excluded_tags}")
            image = await self.client.search(
                included_tags=included_tags,
                excluded_tags=excluded_tags,
                height=height
            )
            if not image:
                print("No image found.")
            return image
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None

    @app_commands.command(name="waifu_image", description="Get a waifu image by tag!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def waifu_image(self, interaction: discord.Interaction, tag: str):
        await interaction.response.defer()  # Defer the interaction response to buy time.

        # Load tags if not already loaded
        if not self.tags:
            await self.fetch_tags()

        # Check if the tag exists in either category
        if not any(tag in tags for tags in self.tags.values()):
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Invalid Tag!",
                    description=f"The tag `{tag}` is not valid. Use `/waifu_tags` to see available tags.",
                    color=discord.Color.red(),
                )
            )
            return

        # Fetch waifu image using the search API with the tag as a filter
        image_url = await self.fetch_image(included_tags=[tag])
        if not image_url:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Error!",
                    description="Could not fetch an image for the provided tag. Please try again later.",
                    color=discord.Color.red(),
                )
            )
            return

        # Suggest a random tag
        suggested_tag = random.choice(self.tags["SFW"] + self.tags["NSFW"])

        # Create embed
        embed = discord.Embed(
            title=f"Here's your waifu image for `{tag}`!",
            color=discord.Color.blurple()
        )
        embed.set_image(url=image_url)
        embed.add_field(name="Suggested Tag", value=f"Try the tag: `{suggested_tag}`")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="waifu_tags", description="Get all available waifu tags!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def waifu_tags(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction response to buy time.

        # Load tags if not already loaded
        if not self.tags:
            await self.fetch_tags()

        if not self.tags["SFW"] and not self.tags["NSFW"]:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Error!",
                    description="Could not fetch tags. Please try again later.",
                    color=discord.Color.red(),
                )
            )
            return

        # Create embed with categorized tags
        embed = discord.Embed(
            title="Available Tags",
            color=discord.Color.green()
        )

        embed.add_field(
            name="SFW Tags",
            value=", ".join(self.tags["SFW"]) if self.tags["SFW"] else "No SFW tags available.",
            inline=False
        )

        embed.add_field(
            name="NSFW Tags",
            value=", ".join(self.tags["NSFW"]) if self.tags["NSFW"] else "No NSFW tags available.",
            inline=False
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="random_waifu", description="Get a random waifu image!")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def random_waifu(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the interaction response to buy time.

        # Fetch random image
        image_url = await self.fetch_image()
        if not image_url:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Error!",
                    description="Could not fetch a random image. Please try again later.",
                    color=discord.Color.red(),
                )
            )
            return

        # Create embed
        embed = discord.Embed(
            title="Here's a random waifu image for you!",
            color=discord.Color.blurple()
        )
        embed.set_image(url=image_url)

        await interaction.followup.send(embed=embed)

    async def cog_unload(self):
        """Ensure we close the WaifuAioClient connection when the cog is unloaded."""
        await self.client.close()

async def setup(bot):
    await bot.add_cog(WaifuCog1(bot))
