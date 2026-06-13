from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime


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


def group_prices_by_time(points: list[PricePoint]) -> dict[datetime, dict[str, float]]:
    prices_by_time: dict[datetime, dict[str, float]] = {}

    for point in points:
        prices_by_time.setdefault(point.timestamp, {})[point.symbol] = point.price

    return prices_by_time
