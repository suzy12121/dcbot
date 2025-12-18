import discord
from discord.ext import commands
from discord import app_commands

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="你好", description="Say hello to the world")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("你好，世界")


    @commands.command()
    async def sendembed(self, ctx):
        msg = discord.Embed(title="標題", description="說明", color=discord.Color.red())
        msg.add_field(name="名字", value="數值", inline=True)
        msg.add_field(name="名字", value="數值", inline=True)
        await ctx.send(embed=msg)


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
