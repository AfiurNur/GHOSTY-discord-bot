import discord
from discord.ext import commands

class ModCog(commands.Cog):
    """Cog to handle message events."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.bot.user:
            return

        # Log messages in the specified channel
        log_channel = self.bot.get_channel(1322056573710893156)
        if log_channel:
            await log_channel.send(f'{message.author.mention} messaged: `{message.content}`')
        
        # Allow other listeners or commands to process the message
        await self.bot.process_commands(message)

    @commands.command()
    async def test(self, ctx):
        """Test command to ensure the cog is working successfully."""
        await ctx.send("***Test command is working!***")

# Setup function to add this cog
async def setup(bot):
    await bot.add_cog(ModCog(bot))
