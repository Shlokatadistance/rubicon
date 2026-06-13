"""Portfolio data loader.

Functions:
- load_prices(tickers, start, end) -> pd.DataFrame
- align_market_hours(df, market_close_times) -> pd.DataFrame
"""
import os
import databento
import pandas as pd
import pathlib

import csv
from dataclasses import dataclass
from datetime import datetime



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
        df:pd.DataFrame = self.query_client.timeseries.get_range(
            dataset=dataset_id,
            symbols=symbols,
            schema=schema,
            start=time_frame["start"],
            end=time_frame["end"],
        ).to_df()
        current_path = pathlib.Path(__file__).parent.parent
        df = df.rename(columns={"close":"price","ts_event":"timestamp"})
        return df.to_csv(f"{current_path}/sample_data.csv")


@dataclass(frozen=True)
class PricePoint:
    timestamp: datetime
    symbol: str
    price: float


def load_price_points_csv(
    path: str,
    timestamp_col: str = "timestamp",
    symbol_col: str = "symbol",
    price_col: str = "price",
) -> list[PricePoint]:
    """
    Load historical prices from a simple CSV.

    Expected shape:
        timestamp,symbol,price
        2026-01-01T09:30:00,AAPL,190.25
    """
    points: list[PricePoint] = []

    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            points.append(
                PricePoint(
                    timestamp=datetime.fromisoformat(row[timestamp_col]),
                    symbol=row[symbol_col],
                    price=float(row[price_col]),
                )
            )

    return points

# x =  FetchMarketData()
# x.fetch_historical_data(symbols="AAPL",schema="OHLCV-1m",dataset_id="EQUS.MINI",time_frame={"start":"2023-11-10T00:00:00","end":"2023-11-20T00:10:00"})