import discord
from discord.ext import commands

class MessageLoggerCog(commands.Cog):
    """Cog to handle message events."""

    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1322056573710893156

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.bot.user:
            return
        if message.content.startswith('!'):
            return

        # Log messages in the specified channel
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(f'**{message.author.name} messaged:** ```{message.content}```')
        
        # Allow other listeners or commands to process the message
        await self.bot.process_commands(message)
    

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return
        if before.content != after.content:
            embed=discord.Embed(title=f"Message edited by {before.author}", description=f"in {before.channel.mention}", color=0xffa200)
            embed.add_field(name=f"Before:", value=f"{before.content}", inline=False)
            embed.add_field(name=f"After:", value=f"{after.content}", inline=True)
            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return
        
        embed = discord.Embed(
            title="Message Deleted",
            description=f"in {message.channel.mention} | Author: {message.author}",
            color=0xffa200
        )
        
        # Check if the message had any content
        if message.content:
            embed.add_field(name="Deleted Message:", value=message.content, inline=False)

        if message.attachments:
            for attachment in message.attachments:
                embed.add_field(name="Attachment:", value=attachment.url, inline=False)

        await channel.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.role):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return
        
        embed = discord.Embed(
        title="Role Created",
        description=f"A new role **{role.name}** has been created.",
        color=0x00ff00
        )
        embed.add_field(name="Role ID", value=role.id, inline=False)
        embed.add_field(name="Role Color", value=str(role.color), inline=True)
        embed.add_field(name="Mentionable", value=str(role.mentionable), inline=True)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        channel = self.bot.get_channel(self.log_channel_id)  # Replace with your log channel ID
        if channel is None:
            return

        embed = discord.Embed(
            title="Role Deleted",
            description=f"The role **{role.name}** has been deleted.",
            color=0xff0000
        )
        embed.add_field(name="Role ID", value=role.id, inline=False)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return
        embed = discord.Embed(
            title="Scheduled Event Created",
            description=f"A new event **{event.name}** has been created.",
            color=0x00ff00
        )
        embed.add_field(name="Event Description", value=event.description or "No description", inline=False)
        embed.add_field(name="Starts At", value=event.start_time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)

        await channel.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_scheduled_event_delete(self, event):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return
        embed = discord.Embed(
        title="Scheduled Event Deleted",
        description=f"The event **{event.name}** has been deleted.",
        color=0xff0000
        )
        embed.add_field(name="Event Description", value=event.description or "No description provided", inline=False)
        embed.add_field(name="Scheduled Start Time", value=event.start_time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)

        if event.end_time:
            embed.add_field(name="Scheduled End Time", value=event.end_time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)

        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_scheduled_event_update(self, before: discord.ScheduledEvent, after: discord.ScheduledEvent):
        channel = self.bot.get_channel(self.log_channel_id)  # Replace with your log channel ID
        if channel is None:
            return

        embed = discord.Embed(
            title="Scheduled Event Updated",
            color=0x00ffff
        )

        if before.name != after.name:
            embed.add_field(name="Name Change", value=f"**Before:** {before.name}\n**After:** {after.name}", inline=False)
        
        if before.description != after.description:
            embed.add_field(
                name="Description Change",
                value=f"**Before:** {before.description or 'No description'}\n**After:** {after.description or 'No description'}",
                inline=False
            )
        
        if before.start_time != after.start_time:
            embed.add_field(
                name="Start Time Change",
                value=f"**Before:** {before.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n**After:** {after.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
                inline=True
            )
        
        if before.end_time != after.end_time:
            embed.add_field(
                name="End Time Change",
                value=f"**Before:** {before.end_time.strftime('%Y-%m-%d %H:%M:%S') if before.end_time else 'No end time'}\n"
                    f"**After:** {after.end_time.strftime('%Y-%m-%d %H:%M:%S') if after.end_time else 'No end time'}",
                inline=True
            )
        
        if before.location != after.location:
            embed.add_field(
                name="Location Change",
                value=f"**Before:** {before.location or 'No location'}\n**After:** {after.location or 'No location'}",
                inline=False
            )

        embed.set_footer(text=f"Event ID: {after.id}")
        await channel.send(embed=embed)


        


# Setup function to add this cog
async def setup(bot):
    await bot.add_cog(MessageLoggerCog(bot))
