import asyncio
from bot.discord_client import bot
from config import Config

async def main():
    """
    Entry point for the Vietnamese Stock Analysis Bot.
    """
    if not Config.DISCORD_TOKEN or not Config.GEMINI_API_KEY:
        print("Error: Required environment variables are missing in .env")
        return

    async with bot:
        # Import and register StockCommands Cog
        from bot.commands import StockCommands
        await bot.add_cog(StockCommands(bot))
        
        # Start bot
        await bot.start(Config.DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is shutting down...")