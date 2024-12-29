import discord
from discord.ext import commands
from discord import app_commands

class testCog(commands.Cog):
    """Cog to handle message events."""

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="test", description="Test slash command.")
    @app_commands.guilds(discord.Object(id=1242396018704908289))  # Replace with your guild ID
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("success!")



# Setup function to add this cog
async def setup(bot):
    await bot.add_cog(testCog(bot))
