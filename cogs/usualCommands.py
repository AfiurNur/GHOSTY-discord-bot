import discord
from discord.ext import commands
from discord import app_commands

guild_id = 1242396018704908289
logging_channel_id = 1322056573710893156

class UsualCommandsCog(commands.Cog):  # Corrected capitalization
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="aboutus", description="About Us.")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def aboutus(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎮 Welcome to Ghosty Sports! 🎮",
            description=(
                "We are a vibrant gaming community dedicated to hosting thrilling events and tournaments "
                "across various games. Whether you're a casual player or a competitive gamer, we have something for everyone!"
            ),
            color=0x1abc9c
        )
        
        embed.add_field(
            name="🏆 **What We Offer:**",
            value=(
                "- **Tournaments:** Regularly hosted competitions with exciting prizes.\n"
                "- **Events:** Fun-filled gaming nights, community challenges, and more.\n"
                "- **Community:** A friendly space to connect, team up, and share your gaming experiences."
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎯 **Our Goals:**",
            value=(
                "1. Build a thriving and inclusive gaming community.\n"
                "2. Provide top-notch tournaments and events for players of all skill levels.\n"
                "3. Celebrate the joy of gaming together!"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🌐 **Get Involved:**",
            value=(
                "👉 Participate in our tournaments.\n"
                "👉 Join our community events.\n"
                "👉 Interact with fellow gamers on our server channels."
            ),
            inline=False
        )

        # Safely handle the guild icon
        if interaction.guild.icon:
            embed.set_footer(text="Thank you for being a part of our community! 💙", icon_url=interaction.guild.icon.url)
        else:
            embed.set_footer(text="Thank you for being a part of our community! 💙")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(UsualCommandsCog(bot))  # Corrected capitalization
