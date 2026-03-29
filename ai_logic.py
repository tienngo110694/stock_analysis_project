from google import genai
import json
import re

class GeminiProcessor:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.5-pro'  # Use a valid model identifier
    async def summarize_request(self, user_input: str):
        """
        Step 2: Summarize Vietnamese natural language into structured data.
        """
        prompt = f"""
        Phân tích yêu cầu sau đây về chứng khoán: "{user_input}"
        Trả về kết quả dưới dạng JSON với các trường:
        - stock_code: Mã cổ phiếu (ví dụ: VNM, FPT)
        - info_needed: Danh sách các loại thông tin yêu cầu (price, financial, fund)
        """
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt
        )
        # Use regex to extract JSON from possible markdown formatting
        try:
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            clean_json = match.group(0) if match else response.text
            return json.loads(clean_json)
        except (json.JSONDecodeError, AttributeError) as e:
            # Fallback in case of parsing error
            return {"stock_code": None,
                     "info_needed": ["price"]}

    async def finalize_analysis(self, raw_data: dict):
        """
        Step 4: Summarize all collected data into a natural language reply.
        """
        prompt = f"""
        Here's the raw data of related financial information: {json.dumps(raw_data, default=str)}
        # ROLE: You are a Senior Financial Analyst Agent for the Vietnamese stock market. Your task is to process raw 'vnstock' data and provide a high-density, structured analysis.
        # CONSTRAINTS (STRICT)
        - TOTAL LENGTH: Must be under 1900 characters (to safely fit Discord's 2,000 limit).
        - STYLE: Extremely concise, professional, and data-driven.
        - FORMAT: Use Bullet Points exclusively for key insights.
        - NO DISCLAIMERS: Skip all financial advice warnings, greetings, and introductory/concluding filler text.

        # INPUT DATA
        You will receive: Ticker, Financial Ratios (P/E, P/B, ROE, etc.), and Technical Indicators.

        # OUTPUT STRUCTURE (Markdown)

        ## [TICKER] - PHÂN TÍCH NHANH
        - **Xu hướng**: [Tăng | Giảm | Đi ngang]
        - **Định giá**: [Rẻ | Hợp lý | Đắt] - [Lý do ngắn gọn]
        - **Chỉ số nổi bật**: [Nêu 1 chỉ số quan trọng nhất]
        - **Kỹ thuật**: [Hỗ trợ/Kháng cự gần nhất]

        ## ĐIỂM TIN CHÍNH
        - **Tăng trưởng**: [1 câu về doanh thu/lợi nhuận]
        - **Rủi ro**: [1 câu về nợ vay hoặc dòng tiền]
        - **Kết luận (Node Insight)**: [Nhận định ngắn gọn cho bước xử lý tiếp theo]
        """
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text