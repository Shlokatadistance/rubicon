"""Portfolio data loader.

Functions:
- load_prices(tickers, start, end) -> pd.DataFrame
- align_market_hours(df, market_close_times) -> pd.DataFrame
"""
import os
import databento


class DatabentoClient:
    def __init__(self):
        self.api_key = os.getenv("DB_API_KEY")

    @property
    def client(self):
        client = databento.Historical(key=self.api_key)
        return client


class FetchMarketData:

    def __init__(self):
        self.query_client = DatabentoClient().client
    
    def fetch_historical_data(
        self,
        symbols: str | list[str],
        schema: str,
        dataset_id: str,
        time_frame: dict[str],
    ):
        df = self.query_client.timeseries.get_range(
            dataset=dataset_id,
            symbols=symbols,
            schema=schema,
            start=time_frame["start"],
            end=time_frame["end"],
        ).to_df()
        return df
