import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

# Constants for guild and logging channel IDs
guild_id = 1242396018704908289
logging_channel_id = 1322056573710893156

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Delete a specific number of messages!")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Clear a specified number of messages from the channel."""
        try:
            # Defer the response to avoid timeout
            await interaction.response.defer()

            if amount < 1:
                await interaction.followup.send(
                    f"{interaction.user.mention}, please specify a value greater than 0.",
                    ephemeral=True
                )
                return

            # Purge messages and provide feedback
            deleted_messages = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(
                f"{interaction.user.mention} deleted {len(deleted_messages)} message(s)."
            )

            # Log the action
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} deleted {len(deleted_messages)} message(s) in {interaction.channel.mention}."
                )

        except Exception as e:
            await interaction.followup.send(
                f"An error occurred: {e}", ephemeral=True
            )

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """Kick a member from the server with a reason."""
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(
                f"{member.mention} has been kicked.\nReason: **{reason}**",
                ephemeral=False
            )

            # Log the action
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} kicked {member.mention}.\nReason: **{reason}**"
                )

        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to kick this member.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """Ban a member from the server with a reason."""
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(
                f"{member.mention} has been banned.\nReason: **{reason}**",
                ephemeral=False
            )

            # Log the action
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} banned {member.mention}.\nReason: **{reason}**"
                )

        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to ban this member.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user by their ID")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: int):
        """Unban a user by their user ID."""
        try:
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user)
            await interaction.response.send_message(
                f"{interaction.user.mention} unbanned {user.name}.", ephemeral=False
            )

            # Log the action
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} unbanned {user.name}."
                )

        except discord.NotFound:
            await interaction.response.send_message("User not found or not banned.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member for a given time")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: int):
        """Timeout a member for a specified duration (in minutes)."""
        try:
            timeout_duration = timedelta(minutes=duration)
            await member.timeout(timeout_duration, reason=f"Timed out by {interaction.user}")
            await interaction.response.send_message(
                f"{interaction.user.mention} has timed out {member.mention} for {duration} minute(s)."
            )

            # Log the action
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} timed out {member.mention} for {duration} minute(s)."
                )

        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to timeout this member.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)


    @app_commands.command(name="warn", description="Warn a member for inappropriate behavior.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        logging_channel = interaction.guild.get_channel(logging_channel_id)
        await interaction.response.send_message(
            f"{member.mention} has been warned for: **{reason}**", ephemeral=False
        )
        if logging_channel:
            await logging_channel.send(
                f"{interaction.user.mention} warned {member.mention}\nReason: **{reason}**"
            )

    @app_commands.command(name="mute", description="Mute a member indefinitely.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            await member.edit(mute=True, reason=reason)
            await interaction.response.send_message(
                f"{member.mention} has been muted.\nReason: **{reason}**", ephemeral=False
            )
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} muted {member.mention}\nReason: **{reason}**"
                )
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to mute this member.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="unmute", description="Unmute a muted member.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        try:
            await member.edit(mute=False)
            await interaction.response.send_message(f"{member.mention} has been unmuted.", ephemeral=False)
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(f"{interaction.user.mention} unmuted {member.mention}.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to unmute this member.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="softban", description="Softban a member to clear their recent messages.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(ban_members=True)
    async def softban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        try:
            await member.ban(reason=reason, delete_message_days=7)
            await interaction.guild.unban(member)
            await interaction.response.send_message(
                f"{member.mention} has been softbanned.\nReason: **{reason}**", ephemeral=False
            )
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} softbanned {member.mention}\nReason: **{reason}**"
                )
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to softban this member.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="lock", description="Lock a channel to prevent messages.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False

        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.response.send_message(f"{channel.mention} has been locked.", ephemeral=False)
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(f"{interaction.user.mention} locked {channel.mention}.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to lock this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="unlock", description="Unlock a channel to allow messages.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None  # Reset to default

        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.response.send_message(f"{channel.mention} has been unlocked.", ephemeral=False)
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(f"{interaction.user.mention} unlocked {channel.mention}.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to unlock this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="slowmode", description="Set a slowmode delay for a channel.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, delay: int):
        channel = interaction.channel
        try:
            await channel.edit(slowmode_delay=delay)
            await interaction.response.send_message(
                f"Slowmode has been set to {delay} seconds in {channel.mention}.", ephemeral=False
            )
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f"{interaction.user.mention} set slowmode to {delay} seconds in {channel.mention}."
                )
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to set slowmode in this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="userinfo", description="View information about a member.")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles if role != interaction.guild.default_role]), inline=False)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command(name="add_role", description="Add role to a specified member.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions()
    async def add_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Assign role to a member in the server"""

        #check if the bot has sufficient permissions
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message(
                "I cannot assign this role because it is higher than or equal to my highest role",
                ephemeral=True
            )
            return
        
        #check if the role is higher than the command issuer
        if interaction.user.top_role <= role and interaction.guild.owner != interaction.user:
            await interaction.response.send_message(
                "You cannot assign a role higher than or equal to your role.",
                ephemeral=True
            )
            return
        
        #Attempt to add the role
        try:
            await member.add_roles(role, reason=f"Assigned by {interaction.user}")
            await interaction.response.send_message(
                f'{interaction.user.mention} has added the role {role.mention} to {member.mention}.',
                ephemeral=False
            )
            logging_channel = interaction.guild.get_channel(logging_channel_id)
            if logging_channel:
                await logging_channel.send(
                    f'{interaction.user.mention} assigned the role {role.mention} to {member.mention}'
                )
        
        #Error handling
        except discord.Forbidden:
            await interaction.response.send_message(
                "I do not have permission to assign the role {role.mention} to {member.mention}",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f'An error occured while assigning the role: {e}',
                ephemeral=True
            )

    @app_commands.command(name="remove_roles", description="Remove role from a specified member.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.checks.has_permissions(manage_roles = True)
    async def remove_roles(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Remove role from a member in the server"""

         #check if the bot has sufficient permissions
        if interaction.guild.me.top_role <= role:
            await interaction.response.send_message(
                "I cannot assign this role because it is higher than or equal to my highest role",
                ephemeral=True
            )
            return
        
        #check if the role is higher than the command issuer
        if interaction.user.top_role <= role and interaction.guild.owner != interaction.user:
            await interaction.response.send_message(
                "You cannot assign a role higher than or equal to your role.",
                ephemeral=True
            )
            return
        
        #Attempt to remove the role
        try:
            await member.remove_roles(role, reason=f"Removed by {interaction.user.mention}")
            await interaction.response.send_message(
                f'{interaction.user.mention} has removed the role {role.mention} from {member.mention}',
                ephemeral = False
            )
            logging_channel = interaction.guild.get_channel(id=guild_id)
            if logging_channel:
                await interaction.response.send_message(
                    f'{interaction.user.mention} has removed the role {role.mention} from {member.mention}',
                    ephemeral=False
                )

        #Error hadnling
        except discord.Forbidden:
            await interaction.response.send_message(
                f'I do not have the permissions to remove the role {role.mention} from {member.mention}',
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f'An error occured while removin the role : {e}',
                ephemeral=True
            )

# Setup function to add this cog
async def setup(bot):
    await bot.add_cog(ModerationCog(bot))