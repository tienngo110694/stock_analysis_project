import pandas as pd
import clickhouse_connect
from config import Config

class ClickHouseStockHandler:
    """
    Handles database operations for storing stock data into ClickHouse.
    """
    def __init__(self):
        self.client = clickhouse_connect.get_client(
            host=Config.CLICKHOUSE_HOST,
            port=Config.CLICKHOUSE_PORT,
            username=Config.CLICKHOUSE_USER,
            password=Config.CLICKHOUSE_PASSWORD,
            database=Config.CLICKHOUSE_DATABASE
        )
        self._initialize_tables()

    def _initialize_tables(self):
        """
        Creates necessary tables in ClickHouse if they do not exist.
        """
        # 1. Stock Prices Table
        self.client.command("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                code String,
                date Date,
                open Nullable(Float64),
                high Nullable(Float64),
                low Nullable(Float64),
                close Nullable(Float64),
                volume Nullable(Int64),
                adLow Nullable(Float64),
                adHigh Nullable(Float64),
                adOpen Nullable(Float64),
                adClose Nullable(Float64),
                adAverage Nullable(Float64),
                nmVolume Nullable(Int64),
                nmValue Nullable(Float64),
                ptVolume Nullable(Int64),
                ptValue Nullable(Float64),
                change Nullable(Float64),
                pctChange Nullable(Float64)
            ) ENGINE = MergeTree()
            ORDER BY (code, date)
        """)

        # 2. Financial Statements Table
        self.client.command("""
            CREATE TABLE IF NOT EXISTS financial_statements (
                code String,
                fiscalDate Date,
                reportType String,
                modelType String,
                itemCode String,
                value Nullable(Float64),
                displayLevel Nullable(Int32),
                displayOrder Nullable(Int32)
            ) ENGINE = MergeTree()
            ORDER BY (code, fiscalDate, reportType, itemCode)
        """)

        # 3. Financial Ratios Table
        self.client.command("""
            CREATE TABLE IF NOT EXISTS financial_ratios (
                code String,
                reportDate Date,
                ratioCode String,
                value Nullable(Float64)
            ) ENGINE = MergeTree()
            ORDER BY (code, reportDate, ratioCode)
        """)

        # 4. Stock Analysis Embeddings (Vector storage for Step 4)
        # Using Array(Float32) for vector storage
        self.client.command("""
            CREATE TABLE IF NOT EXISTS stock_analysis_vectors (
                code String,
                analysis_date DateTime DEFAULT now(),
                analysis_text String,
                vector Array(Float32),
                metadata String
            ) ENGINE = MergeTree()
            ORDER BY (code, analysis_date)
        """)

    def insert_stock_data(self, data_dict):
        """
        Inserts data from StockDataProvider.get_comprehensive_data() into ClickHouse.
        """
        # Insert Stock Prices
        df_prices = data_dict.get('stock_prices')
        if df_prices is not None and not df_prices.empty:
            if 'date' in df_prices.columns:
                df_prices['date'] = pd.to_datetime(df_prices['date'])
            valid_cols = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 
                         'adLow', 'adHigh', 'adOpen', 'adClose', 'adAverage', 
                         'nmVolume', 'nmValue', 'ptVolume', 'ptValue', 'change', 'pctChange']
            insert_df = df_prices[[c for c in valid_cols if c in df_prices.columns]]
            self.client.insert_df('stock_prices', insert_df)

        # Insert Financial Ratios
        df_ratios = data_dict.get('financial_ratios')
        if df_ratios is not None and not df_ratios.empty:
            if 'reportDate' in df_ratios.columns:
                df_ratios['reportDate'] = pd.to_datetime(df_ratios['reportDate'])
            
            if 'ratioCode' not in df_ratios.columns:
                id_vars = [c for c in ['code', 'reportDate'] if c in df_ratios.columns]
                df_ratios = df_ratios.melt(id_vars=id_vars, var_name='ratioCode', value_name='value')
            
            valid_cols = ['code', 'reportDate', 'ratioCode', 'value']
            insert_df = df_ratios[[c for c in valid_cols if c in df_ratios.columns]]
            self.client.insert_df('financial_ratios', insert_df)

        # Insert Financial Statements
        df_statements = data_dict.get('financial_statements')
        if df_statements is not None and not df_statements.empty:
            if 'fiscalDate' in df_statements.columns:
                df_statements['fiscalDate'] = pd.to_datetime(df_statements['fiscalDate'])
            
            valid_cols = ['code', 'fiscalDate', 'reportType', 'modelType', 'itemCode', 'value', 'displayLevel', 'displayOrder']
            insert_df = df_statements[[c for c in valid_cols if c in df_statements.columns]]
            self.client.insert_df('financial_statements', insert_df)

    def insert_analysis_vector(self, code, text, vector, metadata=None):
        """
        Inserts analysis result and its embedding vector.
        """
        data = [[code, text, vector, metadata or ""]]
        self.client.insert('stock_analysis_vectors', data, column_names=['code', 'analysis_text', 'vector', 'metadata'])

def save_data_after_provider(stock_code, start_date=None, end_date=None):
    """
    Convenience function to fetch and save data.
    """
    from data_collectors.financial_provider import StockDataProvider
    
    provider = StockDataProvider(stock_code)
    data = provider.get_comprehensive_data(start_date=start_date, end_date=end_date)
    
    handler = ClickHouseStockHandler()
    handler.insert_stock_data(data)
    print(f"Successfully saved data for {stock_code} to ClickHouse.")

if __name__ == "__main__":
    # Example usage
    # save_data_after_provider("VND", start_date="2023-01-01", end_date="2023-12-31")
    pass
