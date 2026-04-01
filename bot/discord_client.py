import discord
from discord.ext import commands
from config import Config
import aiohttp

class StockBot(commands.Bot):
    """
    Step 1: Discord bot configuration.
    """
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.session = None

    async def setup_hook(self):
        # Initialize a persistent session for the bot's lifetime
        self.session = aiohttp.ClientSession()
        # Load extensions/commands
        # self.load_extension('bot.commands') # If I separate it

    async def on_ready(self):
        print(f'Bot {self.user} is ready and listening for stock requests!')

    async def close(self):
        if self.session:
            await self.session.close()
        await super().close()

bot = StockBot()
