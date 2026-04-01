from discord.ext import commands
import json
from data_collectors.financial_provider import StockDataProvider
from database.clickhouse_client import ClickHouseStockHandler
from ai.gemini_analyst import GeminiAnalyst
from ai.advisor import StockAdvisor
from ai.embeddings import EmbeddingProcessor
from config import Config

class StockCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = GeminiAnalyst()
        self.advisor = StockAdvisor()
        self.ch_handler = ClickHouseStockHandler()
        self.embed_processor = EmbeddingProcessor()

    @commands.command(name="ingest")
    async def ingest_stock(self, ctx, code: str):
        """
        Step 0: Get financial data and insert into ClickHouse.
        """
        code = code.upper().strip()
        async with ctx.typing():
            provider = StockDataProvider(code)
            # Fetch quarterly report by default
            data = provider.get_comprehensive_data()
            if not any(not df.empty for df in data.values()):
                await ctx.send(f"❌ Không tìm thấy dữ liệu cho mã `{code}`.")
                return

            self.ch_handler.insert_stock_data(data)
            await ctx.send(f"✅ Đã tải dữ liệu của mã `{code}` vào ClickHouse thành công.")

    @commands.command(name="stock")
    async def analyze_stock(self, ctx, *, user_request: str):
        """
        Step 1 & 2.1: Analyze request and trigger processing flow.
        """
        async with ctx.typing():
            # Step 2: Use Gemini to summarize the request
            summary = await self.ai.summarize_user_request(user_request)
            code = summary.get("stock_code")
            
            if not code or code == "null":
                await ctx.send("⚠️ Xin lỗi, mình không tìm thấy mã chứng khoán trong câu hỏi của bạn.")
                return
            
            code = code.upper()

            # Trigger Webhook for n8n Flow (Step 2.1)
            if Config.N8N_WEBHOOK_URL:
                payload = {
                    "stock_code": code,
                    "user_query": user_request,
                    "analyst_config": summary.get("analysis_required")
                }
                async with self.bot.session.post(Config.N8N_WEBHOOK_URL, json=payload) as resp:
                    if resp.status in [200, 201]:
                        await ctx.send(f"🚀 Một yêu cầu phân tích chuyên sâu cho `{code}` đã được gửi lên n8n!")
                    else:
                        await ctx.send(f"⚠️ Không thể gửi yêu cầu lên n8n. Đang xử lý trực tiếp...")
                        # Optional: Here you can implement direct fallback if n8n is down
            else:
                await ctx.send(f"⚠️ N8N_WEBHOOK_URL chưa được cấu hình. Đang thử phân tích trực tiếp...")

    @commands.command(name="full_analysis")
    async def full_analysis(self, ctx, code: str):
        """
        Directly execute Step 2.1-3 from the bot (for testing or local use).
        """
        code = code.upper().strip()
        async with ctx.typing():
            # Step 2.1: Financial (assuming data in CH)
            # In a real scenario, you'd pull this from CH. Let's mocks it or use provider directly.
            provider = StockDataProvider(code)
            data = provider.get_comprehensive_data()
            fin_analysis = await self.ai.analyze_financials(code, {"data": "..."}) 
            
            # Step 2.2 & 2.3 (Mocks/Tool Search)
            macro_analysis = await self.ai.analyze_macro_industry(code, "Kinh tế VN đang ổn định...")
            news_analysis = await self.ai.analyze_stock_news(code, "Tin tức về lợi nhuận quý này...")
            
            # Step 3: Advisor
            final_advice = await self.advisor.generate_advice(code, fin_analysis, macro_analysis, news_analysis)
            
            # Step 4: Embed and Store
            vector = self.embed_processor.get_embedding(final_advice)
            if vector:
                self.ch_handler.insert_analysis_vector(code, final_advice, vector)
                
            await ctx.send(final_advice)

async def setup(bot):
    await bot.add_cog(StockCommands(bot))
