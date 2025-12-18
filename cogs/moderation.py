from __future__ import annotations 
import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="clear", description="Clear a specific amount of messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete_msg(self, interaction: discord.Interaction, amount: int):
        if amount < 1:
            await interaction.response.send_message("Please enter a number greater than 0.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"✅ Deleted {len(deleted)} messages.", ephemeral=True)


    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_member(self, interaction: discord.Interaction, member: discord.Member):
        if member == interaction.user:
            await interaction.response.send_message("You cannot kick yourself!", ephemeral=True)
            return
        
        if member.top_role >= interaction.guild.me.top_role:
             await interaction.response.send_message("I cannot kick this member (they have a higher or equal role).", ephemeral=True)
             return

        await member.kick()
        await interaction.response.send_message(f"{member.mention} has been kicked.", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member for a specific duration")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(minutes="Minutes to timeout", reason="Reason for the timeout")
    async def timeout_member(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = None):
        if member == interaction.user:
            return await interaction.response.send_message("You cannot timeout yourself!", ephemeral=True)

        if member.top_role >= interaction.guild.me.top_role:
            return await interaction.response.send_message("I cannot timeout this member (higher/equal role).", ephemeral=True)

        if minutes > 40320: # 28 days
            return await interaction.response.send_message("Timeout cannot exceed 28 days.", ephemeral=True)

        try:
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            await interaction.response.send_message(
                f"⏳ {member.mention} has been timed out for {minutes} minutes.\n**Reason:** {reason or 'No reason provided.'}", 
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to timeout this member.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)


    @app_commands.command(name="untimeout", description="Remove a timeout from a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout_member(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        await interaction.response.send_message(f"✅ Removed timeout for {member.mention}.", ephemeral=True)

 
    @app_commands.command(name="debug_timeout", description="Check why timeout might be failing")
    async def debug_timeout(self, interaction: discord.Interaction, member: discord.Member):
        guild = interaction.guild
        bot_member = guild.me
        
        has_moderate_perm = bot_member.guild_permissions.moderate_members
        bot_pos = bot_member.top_role.position
        target_pos = member.top_role.position
        hierarchy_check = bot_pos > target_pos
        
        is_owner = member.id == guild.owner_id
        is_admin = member.guild_permissions.administrator

        results = [
            f"🔍 **Diagnostic for {member.display_name}:**",
            f"- Bot has 'Moderate Members' perm: {'✅' if has_moderate_perm else '❌'}",
            f"- Bot position ({bot_pos}) > Target position ({target_pos}): {'✅' if hierarchy_check else '❌'}",
            f"- Target is Server Owner: {'⚠️ Yes (Immune)' if is_owner else '✅ No'}",
            f"- Target has Admin perm: {'⚠️ Yes (Often Immune)' if is_admin else '✅ No'}",
        ]

        await interaction.response.send_message("\n".join(results), ephemeral=True)

  
    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
