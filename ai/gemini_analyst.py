import json
import re
from google import genai
from config import Config

class GeminiAnalyst:
    """
    Handles AI analysis for financial data, news, and macro-economics.
    """
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.pro_model = Config.GEMINI_MODEL_PRO
        self.flash_model = Config.GEMINI_MODEL_FLASH

    async def summarize_user_request(self, user_input: str):
        """
        Step 2: Parse natural language into structured stock code and info types.
        """
        prompt = f"""
        Phân tích yêu cầu tiếng Việt sau: "{user_input}"
        Trả về JSON:
        {{
            "stock_code": "Mã cổ phiếu (VD: FPT)",
            "analysis_required": ["financial", "news", "macro_industry"]
        }}
        """
        return await self._generate_structured_json(self.flash_model, prompt)

    async def analyze_financials(self, code: str, financial_data: dict):
        """
        Step 2.1: Analyze financial data from ClickHouse.
        """
        prompt = f"""
        Phân tích dữ liệu tài chính của mã `{code}` sau đây:
        {json.dumps(financial_data, indent=2, default=str)}
        
        Nhiệm vụ: Tìm các điểm mạnh/yếu tài chính, xu hướng doanh thu/lợi nhuận, và định giá (P/E, P/B).
        Yêu cầu: Viết ngắn gọn, súc tích bằng tiếng Việt.
        """
        return await self._generate_text(self.pro_model, prompt)

    async def analyze_macro_industry(self, code: str, context_info: str):
        """
        Step 2.2: Analyze macro economy and industry news.
        """
        prompt = f"""
        Phân tích kinh tế vĩ mô và ngành liên quan đến mã `{code}` tại Việt Nam.
        Thông tin ngữ cảnh: {context_info}
        
        Yêu cầu: Nhận định tác động tích cực/tiêu cực từ vĩ mô và triển vọng ngành.
        """
        return await self._generate_text(self.pro_model, prompt)

    async def analyze_stock_news(self, code: str, news_info: str):
        """
        Step 2.3: Analyze latest news about specific stock.
        """
        prompt = f"""
        Phân tích các tin tức mới nhất về mã `{code}`:
        {news_info}
        
        Yêu cầu: Tóm tắt các sự kiện đáng chú ý (M&A, dự án mới, thay đổi lãnh đạo...).
        """
        return await self._generate_text(self.pro_model, prompt)

    async def _generate_text(self, model, prompt):
        response = await self.client.aio.models.generate_content(model=model, contents=prompt)
        return response.text

    async def _generate_structured_json(self, model, prompt):
        response = await self.client.aio.models.generate_content(
            model=model, 
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        try:
            return json.loads(response.text)
        except Exception:
            # Fallback regex if needed
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            return json.loads(match.group(0)) if match else {}