import discord
from discord.ext import commands, tasks
import os
import secret
import asyncio
from itertools import cycle
import pyfiglet

# Define ANSI color codes
RED = "\033[31m"

# Create ASCII text art
ascii_art_1 = pyfiglet.figlet_format("Afiur Nur", font = "standard" )
ascii_art_2 = pyfiglet.figlet_format("Bot Ready", font = "standard" )
ascii_art_3 = pyfiglet.figlet_format("Commands Synced", font = "standard")


print(f"{RED}\n*******************************************************************************\n")

print(ascii_art_1)

print(f"\n*******************************************************************************\n")


# Initialize the bot with all intents enabled
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot_statuses = cycle(["GHOSTY SPORTS"])
@tasks.loop(seconds=5)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))


@bot.event
async def on_ready():
    print(f'Loaded Cogs: 23')

    print(f"\n*******************************************************************************\n")

    print(f'Logged in as {bot.user}        ✅')
    print(f'Status: Bot is ready           ✅')
    print(ascii_art_2)

    print(f"\n*******************************************************************************\n")

    change_bot_status.start()
    bot_status_channel = bot.get_channel(1242479081153630238)
    await bot_status_channel.send(f'{bot.user.mention} **is successfully online ✅**')

    # Sync slash commands globally or for a specific guild
    try:
        guild = discord.Object(id=secret.GuildID)  # Use your testing guild ID
        synced = await bot.tree.sync(guild=guild)  # Sync commands to a specific guild
        print(f"Synced {len(synced)} commands to guild {guild.id}")
        
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(ascii_art_3)

    print(f"\n*******************************************************************************\n")

    print(
        "Bucket List:\n"
        "- UserUpdateLogger [DONE]✅\n"
        "- cogManager [DONE]✅\n"
        "- messageLogger [DONE]✅\n"
        "- verification [DONE]✅\n"
        "- moderation [DONE]✅\n"
        "- spotify [DONE]✅\n"
        "- welcome [Not Completed]❌\n"
        "- music [DONE]✅\n"
        "- responseToCertainWords [Not Completed]❌\n"
        "- ChatAI [Not Completed]❌\n"
        "- UseDifferentAPI [DONE]✅\n"
    )


# Load all cogs dynamically from multiple folders
async def load_cogs():
    cog_folders = ['./cogs', './cogs/nsfw_commands']  # Add all the cog folders you want to load
    
    for folder in cog_folders:
        # Loop through all files in the current folder
        for filename in os.listdir(folder):
            if filename.endswith('.py'):
                try:
                    # Convert folder path to the correct dotted format and load the cog
                    await bot.load_extension(f'{folder.replace("./", "").replace("/", ".")}.{filename[:-3]}')
                    print(f"Loaded cog: {filename} ✅")     
                except Exception as e:
                    print(f"Failed to load cog {filename} ❌: {e}")

# Main function to manage bot lifecycle
async def main():
    async with bot:
        await load_cogs()  # Load cogs from all folders
        await bot.start(secret.DiscordToken)

# Run the bot
asyncio.run(main())
