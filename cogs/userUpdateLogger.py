import discord
from discord.ext import commands

class UserUpdateLoggerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Replace with the ID of the channel where logs should be sent
        self.log_channel_id = 1323300367546581102

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return  # Log channel not found
        
        embed = discord.Embed(
            title="User Update Log",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_author(name=f"{after} ({after.id})", icon_url=after.display_avatar.url)

        if before.avatar != after.avatar:
            embed.add_field(name="Avatar Changed", value="User updated their avatar.")
            embed.set_thumbnail(url=after.avatar.url)

        if before.username != after.username:
            embed.add_field(name="Username Changed", value=f"**Before:** {before.username}\n**After:** {after.username}")

        if embed.fields:  # Ensure there are changes to log
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return  # Log channel not found
        
        embed = discord.Embed(
            title="Member Update Log",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_author(name=f"{after} ({after.id})", icon_url=after.display_avatar.url)

        # Check for nickname changes
        if before.nick != after.nick:
            embed.add_field(name="Nickname Changed", value=f"**Before:** {before.nick or 'None'}\n**After:** {after.nick or 'None'}")

        # Check for role changes
        before_roles = set(before.roles)
        after_roles = set(after.roles)

        added_roles = after_roles - before_roles
        removed_roles = before_roles - after_roles

        if added_roles:
            embed.add_field(
                name="Roles Added",
                value="\n".join([role.mention for role in added_roles]),
                inline=False
            )

        if removed_roles:
            embed.add_field(
                name="Roles Removed",
                value="\n".join([role.mention for role in removed_roles]),
                inline=False
            )

        if embed.fields:  # Ensure there are changes to log
            await channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel is None:
            return

        await channel.send(f'{member.name} has left the server.')

async def setup(bot):
    await bot.add_cog(UserUpdateLoggerCog(bot))
