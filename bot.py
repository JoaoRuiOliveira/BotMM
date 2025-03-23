import os
import discord 
from discord.ext import commands
import pathlib
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / 'cogs'
DTOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'Bot is ready! {bot.user}')

    for cmd_file in CMDS_DIR.glob('*.py'):
        if cmd_file.name == 'player.py':
            await bot.load_extension(f'cogs.{cmd_file.name[:-3]}')

@bot.command(name='load')
async def load(ctx, cog: str):
    await bot.load_extension(f"cogs.{cog.lower()}")
        
@bot.command(name='unload')
async def unload(ctx, cog: str):
    await bot.unload_extension(f"cogs.{cog.lower()}")
        
@bot.command(name='reload')
async def reload(ctx, cog: str):
    await bot.reload_extension(f"cogs.{cog.lower()}")

@bot.command(name='sync')
async def sync(ctx, cog: str):
    try:
        synced = await bot.tree.sync()  # Sync globally
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

bot.run(DTOKEN)