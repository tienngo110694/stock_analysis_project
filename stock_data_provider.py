import requests
import pandas as pd
import json

class StockDataProvider:
    """
    A unified interface to fetch financial statements, prices, models, and ratios
    for a specific stock from VNDirect APIs.
    """
    
    BASE_URL = "https://api-finfo.vndirect.com.vn/v4"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    def __init__(self, stock_code):
        self.stock_code = stock_code.upper().strip()

    def get_comprehensive_data(self, start_date=None, end_date=None, report_type="QUARTER", report_date=None):
        """
        Returns a dictionary containing all related data frames.
        
        Args:
            start_date (str): format YYYY-MM-DD for stock prices
            end_date (str): format YYYY-MM-DD for stock prices
            report_type (str): "QUARTER" or "ANNUAL"
            report_date (str): format YYYY-MM-DD for specific ratios
        """
        return {
            "financial_statements": self.fetch_financial_statements(report_type),
            "stock_prices": self.fetch_stock_price(start_date, end_date) if start_date and end_date else pd.DataFrame(),
            "financial_models": self.fetch_financial_models(),
            "financial_ratios": self.fetch_financial_ratios(report_date) if report_date else pd.DataFrame()
        }

    def fetch_financial_statements(self, report_type, fiscal_dates=None, model_types="1", size=2000):
        report_key = str(report_type).upper().strip()
        report_aliases = {
            "Q": "QUARTER", "QUARTERLY": "QUARTER", "QUARTER": "QUARTER",
            "A": "ANNUAL", "Y": "ANNUAL", "YEARLY": "ANNUAL", "ANNUAL": "ANNUAL",
        }
        report_type = report_aliases.get(report_key)
        if not report_type:
            raise ValueError(f"Invalid report_type: {report_key}")

        url = f"{self.BASE_URL}/financial_statements"
        query_parts = [f"code:{self.stock_code}", f"reportType:{report_type}", f"modelType:{model_types}"]
        if fiscal_dates:
            query_parts.append(f"fiscalDate:{','.join(fiscal_dates)}")

        params = {"q": "~".join(query_parts), "sort": "fiscalDate:desc", "size": size}
        return self._make_request(url, params)

    def fetch_stock_price(self, start_date, end_date, size=1000):
        url = f"{self.BASE_URL}/stock_prices"
        params = {
            "sort": "date",
            "q": f"code:{self.stock_code}~date:gte:{start_date}~date:lte:{end_date}",
            "size": size,
            "page": 1
        }
        return self._make_request(url, params, date_col="date")

    def fetch_financial_models(self, model_types="1", display_levels="0,1,2,3", size=999):
        notes = "TT199/2014/TT-BTC,TT334/2016/TT-BTC,TT49/2014/TT-NHNN,TT202/2014/TT-BTC"
        url = f"{self.BASE_URL}/financial_models"
        params = {
            "sort": "displayOrder:asc",
            "q": f"codeList:{self.stock_code}~modelType:{model_types}~note:{notes}~displayLevel:{display_levels}",
            "size": size,
        }
        return self._make_request(url, params)

    def fetch_financial_ratios(self, report_date):
        ratio_codes = [
            "NET_SALES_TR_GRYOY", "NET_PROFIT_TR_GRYOY", "OPERATING_EBIT_TR_GRYOY",
            "GROSS_MARGIN_TR", "ROAA_TR_AVG5Q", "ROAE_TR_AVG5Q", "DEBT_TO_EQUITY_AQ",
            "DIVIDEND_YIELD", "CFO_TO_SALES_TR", "INTEREST_COVERAGE_TR", "CPS_AQ"
        ]
        url = f"{self.BASE_URL}/ratios"
        params = {"q": f"code:{self.stock_code}~ratioCode:{','.join(ratio_codes)}~reportDate:{report_date}"}
        return self._make_request(url, params, date_col="reportDate")

    def _make_request(self, url, params, date_col=None):
        """Helper to handle requests and dataframe conversion."""
        try:
            response = requests.get(url, params=params, headers=self.HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json().get("data", [])
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(data)
            if date_col and date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col])
            return df
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            return pd.DataFrame()
