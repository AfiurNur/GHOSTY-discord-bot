import discord
from discord import File
from easy_pil import Editor, load_image_async, Font
from discord.ext import commands
import random

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"Member {member.name}#{member.discriminator} joined the server!")
        
        random_bg = ['./asset/b1.png', './asset/b2.png', './asset/b3.png', './asset/b4.png', './asset/b5.png']
        bg_random = random.choice(random_bg)
        
        # Get the welcome channel
        channel = self.bot.get_channel(1242401109059043378)
        
        # Prepare the background image
        background = Editor(str(bg_random))
        
        # Load the profile image asynchronously
        profile_image = await load_image_async(str(member.avatar.url))
        
        # Resize the profile image and create a circle image
        profile = Editor(profile_image).resize((150, 150)).circle_image()
        
        # Fonts for the text
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=20, variant="light")
        
        # Paste profile image onto the background and add effects
        background.paste(profile, (325, 90))
        background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)
        
        # Add text onto the background
        background.text((400, 260), f"Welcome to {member.guild.name}", color="white", font=poppins, align="center")
        background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")
        
        # Create a File object for the image
        file = File(fp=background.image_bytes, filename=str(bg_random))
        
        # Send the welcome message and image to the channel
        await channel.send(f"Hello {member.mention}! Welcome To **{member.guild.name}. For more information go to #📑-rules")
        await channel.send(file=file)

# The setup function for loading the cog
async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
