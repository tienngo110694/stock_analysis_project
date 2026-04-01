from google import genai
from config import Config

class StockAdvisor:
    """
    Final Gemini node to summarize all analyses and provide advice.
    """
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model = Config.GEMINI_MODEL_PRO

    async def generate_advice(self, code, financial_analysis, macro_analysis, news_analysis):
        """
        Step 3: Aggregate all analyses and provide final Buy/Sell/Neutral advice.
        """
        prompt = f"""
        # ROLE: Chuyên gia phân tích chứng khoán cấp cao tại Việt Nam.
        # INPUT:
        - Mã cổ phiếu: `{code}`
        - Phân tích tài chính: {financial_analysis}
        - Phân tích vĩ mô & ngành: {macro_analysis}
        - Phân tích tin tức: {news_analysis}
        
        # TASK:
        Tổng hợp tất cả thông tin trên để đưa ra nhận định cuối cùng.
        
        # OUTPUT STRUCTURE (REQUIRED):
        1. **KHUYẾN NGHỊ**: [MUA | BÁN | THEO DÕI] tại vùng giá cụ thể (nếu có).
        2. **LÝ DO CHI TIẾT**:
           - **Phân tích tài chính**: (Tóm tắt điểm chính)
           - **Phân tích vĩ mô**: (Tóm tắt điểm chính)
           - **Phân tích ngành**: (Tóm tắt điểm chính)
        3. **RỦI RO CẦN LƯU Ý**: (Các yếu tố tiêu cực có thể xảy ra)
        
        # STYLE: Chuyên nghiệp, khách quan, sử dụng tiếng Việt.
        """
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
