import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True 
intents.guild_messages = True

bot = commands.Bot(command_prefix='$', intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f"{bot.user} logged in!")

# --- 🧹 THE MAGIC FIX COMMAND ---
@bot.command()
async def fixsync(ctx):
    msg = await ctx.send("⏳ Fixing duplicates... (This might take a few seconds)")
    
    # STEP 1: WIPE GLOBAL COMMANDS
    # We clear the internal list and sync "nothing" to Discord Global.
    # This removes the stubborn global duplicates.
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    
    # STEP 2: RELOAD COGS
    # Since we just wiped the commands from memory, we re-read the files.
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.reload_extension(f'cogs.{filename[:-3]}')
            
    # STEP 3: SYNC TO GUILD ONLY
    # Now we register the commands ONLY to this server (Instant & No duplicates).
    bot.tree.copy_global_to(guild=ctx.guild)
    await bot.tree.sync(guild=ctx.guild)
    
    await msg.edit(content="✅ **Duplicates Fixed!** Global commands wiped, Guild commands active.")


app = Flask('')

@app.route('/')
def home():
    return "上線了"

def run_flask():
  
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

async def main():
   
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
 
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == '__main__':
  	asyncio.run(main())
