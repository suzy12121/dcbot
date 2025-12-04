import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "bot" in message.content.lower() and "hi" in message.content.lower():
        await message.channel.send(f"你好 {message.author.display_name}!")
        
    await bot.process_commands(message)
    
@bot.command()
async def hello(ctx):
  await ctx.send(f"你好啊{ctx.author.mention}")


bot.run(token)