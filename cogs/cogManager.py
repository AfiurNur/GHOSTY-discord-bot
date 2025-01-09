import discord
from discord.ext import commands
import os

class CogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load", help="Loads a cog. Admin only.")
    @commands.is_owner()  # Restrict this command to the bot owner
    async def load_cog(self, ctx, cog: str):
        """Loads a specified cog."""
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Successfully loaded `{cog}`.")
            print(f"Successfully loaded `{cog}`.")
        except Exception as e:
            await ctx.send(f"Failed to load `{cog}`: {e}")
            print(f"Failed to load `{cog}`: {e}")

    @commands.command(name="unload", help="Unloads a cog. Admin only.")
    @commands.is_owner()
    async def unload_cog(self, ctx, cog: str):
        """Unloads a specified cog."""
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"Successfully unloaded `{cog}`.")
            print(f"Successfully unloaded `{cog}`.")
        except Exception as e:
            await ctx.send(f"Failed to unload `{cog}`: {e}")
            print(f"Failed to unload `{cog}`: {e}")

    @commands.command(name="reload", help="Reloads a cog. Admin only.")
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        """Reloads a specified cog."""
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Successfully reloaded `{cog}`.")
            print(f"Successfully reloaded `{cog}`.")
        except Exception as e:
            await ctx.send(f"Failed to reload `{cog}`: {e}")
            print(f"Failed to reload `{cog}`: {e}")

async def setup(bot):
    await bot.add_cog(CogManager(bot))
