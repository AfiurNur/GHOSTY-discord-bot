import discord
from discord.ext import commands
import os
import secret
import asyncio

# Initialize the bot with all intents enabled
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}        ✅')
    print(f'Status: Bot is ready           ✅')

    # Sync slash commands globally or for a specific guild
    try:
        guild = discord.Object(id=secret.GuildID)  # Use your testing guild ID
        synced = await bot.tree.sync(guild=guild)  # Sync commands to a specific guild
        print(f"Synced {len(synced)} commands to guild {guild.id}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Load all cogs dynamically
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

# Main function to manage bot lifecycle
async def main():
    async with bot:
        await load_cogs()
        await bot.start(secret.DiscordToken)

# Run the bot
asyncio.run(main())
