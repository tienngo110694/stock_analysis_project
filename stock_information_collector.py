import asyncio
import pandas as pd
from datetime import datetime, timedelta
from vnstock import Company, Quote, Finance

class StockInformationCollect:
    """
    Step 3: Collects related financial info using the vnstock library.
    """
    def __init__(self):
        pass

    async def collect_data(self, stock_code: str, info_types: list):
        data = {"stock": stock_code}
        loop = asyncio.get_event_loop()
        
        # vnstock is synchronous, so we run the fetching logic in an executor
        def fetch_sync():
            results = {}
            if "price" in info_types:
                results["price_info"] = self._fetch_price(stock_code)
            if "financial" in info_types:
                results["financial_info"] = self._fetch_financials(stock_code)
            if "company" in info_types or "fund" in info_types:
                results["company_info"] = self._fetch_company_info(stock_code)
            return results

        fetched_results = await loop.run_in_executor(None, fetch_sync)
        data.update(fetched_results)
        return data

    def _fetch_price(self, symbol):
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
            q = Quote(symbol=symbol, source='VCI')
            df = q.history(start=start_date, end=end_date, interval="1D")
            if isinstance(df, pd.DataFrame) and not df.empty:
                df.columns = df.columns.map(str)
                # Return last 5 days of data for trend analysis
                return df.tail(30).to_dict(orient='records')
            return "Dữ liệu giá không khả dụng."
        except Exception as e:
            return f"Lỗi khi truy xuất dữ liệu giá: {str(e)}"

    def _fetch_financials(self, symbol):
        try:
            f = Finance(symbol=symbol, source='VCI')
            df = f.ratio(period='quarter', lang='vi')
            if isinstance(df, pd.DataFrame) and not df.empty:
                # Convert MultiIndex to string labels to ensure JSON compatibility
                df.index = df.index.map(str)
                df.columns = df.columns.map(str)
                return df.to_dict()
            return "Chỉ số tài chính không khả dụng."
        except Exception as e:
            return f"Lỗi khi truy xuất chỉ số tài chính: {str(e)}"

    def _fetch_company_info(self, symbol):
        try:
            # Using the Company class directly to fetch profile/overview information
            c = Company(symbol=symbol, source='VCI')
            result = c.overview()
            
            if isinstance(result, pd.DataFrame) and not result.empty:
                # Convert MultiIndex to string labels to ensure JSON compatibility
                result.index = result.index.map(str)
                result.columns = result.columns.map(str)
                return result.to_dict()
            elif isinstance(result, dict):
                return result
            return "Hồ sơ công ty không khả dụng."
        except Exception as e:
            return f"Lỗi khi truy xuất hồ sơ công ty: {str(e)}"