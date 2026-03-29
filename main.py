import discord
from discord.ext import commands
from ai_logic import GeminiProcessor
from stock_information_collector import StockInformationCollect
import os
from dotenv import load_dotenv
import aiohttp
import json

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

if not TOKEN or not GEMINI_KEY:
    print("Lỗi: Không tìm thấy DISCORD_TOKEN hoặc GEMINI_API_KEY trong file .env")
    exit(1)

if "your_discord_bot_token_here" in TOKEN or "your_gemini_api_key_here" in GEMINI_KEY:
    print("Lỗi: Bạn cần thay thế Token và API Key thật vào file .env thay vì sử dụng văn bản mẫu.")
    exit(1)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
ai = GeminiProcessor(GEMINI_KEY)
collector = StockInformationCollect()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

@bot.event
async def on_command_error(ctx, error):
    """
    Handles errors when a command is not found or fails.
    """
    if isinstance(error, commands.CommandNotFound):
        # Optional: Automatically try to process !TICKER as !stock TICKER
        ticker = ctx.invoked_with
        if ticker and ticker.isupper() and 3 <= len(ticker) <= 5:
            stock_command = bot.get_command("stock")
            await ctx.invoke(stock_command, user_request=ticker)
        else:
            await ctx.send(f"⚠️ Không tìm thấy lệnh `!{ctx.invoked_with}`. Hãy thử dùng `!stock {ctx.invoked_with}`")
    else:
        # Log other errors to console
        print(f"Xảy ra lỗi: {error}")

@bot.command(name="stock")
async def analyze_stock(ctx, *, user_request: str):
    """
    Flow implementation
    """
    async with ctx.typing():
        try:
            # Step 2: Summarize request via Gemini
            summary = await ai.summarize_request(user_request)
            stock_code = summary.get("stock_code")
            info_needed = summary.get("info_needed", ["price"])

            # Step 3: Collect data
            raw_data = await collector.collect_data(stock_code, info_needed)

            # Step 4: Gửi kết quả qua webhook lên n8n để trigger flow
            if not N8N_WEBHOOK_URL or not N8N_WEBHOOK_URL.startswith("http"):
                await ctx.send("❌ Lỗi: N8N_WEBHOOK_URL chưa được cấu hình hoặc không hợp lệ trong .env")
                return

            payload = {
                "source": "discord_bot",
                "user": str(ctx.author),
                "user_request": user_request,
                "stock_code": stock_code,
                "data": raw_data
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    N8N_WEBHOOK_URL, 
                    data=json.dumps(payload, default=str), 
                    headers={'Content-Type': 'application/json'}, 
                    timeout=10
                ) as response:
                    if response.status in [200, 201]:
                        await ctx.send(f"✅ Đã lấy dữ liệu cho mã `{stock_code}` và gửi lên n8n thành công để xử lý!")
                    else:
                        await ctx.send(f"⚠️ Đã lấy được dữ liệu nhưng gửi lên n8n thất bại (Mã lỗi: {response.status}).")
                
        except Exception as e:
            await ctx.send(f"Đã xảy ra lỗi khi xử lý yêu cầu: {str(e)}")

if __name__ == "__main__":
    bot.run(TOKEN)