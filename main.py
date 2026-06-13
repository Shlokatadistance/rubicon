"""Main CLI entrypoint for Rubicon portfolio risk simulator.

Orchestrates:
- CSV price loading (price_data)
- Per-symbol Kalman filtering (kalman)
- Future: MC simulation + risk metrics
"""

from __future__ import annotations

from price_data import load_price_points_csv, group_prices_by_time
from tmp.kalman import StockKalmanFilter


def run_kalman_on_csv(csv_path: str) -> None:
    """Load prices from CSV and run Kalman filter per symbol."""
    points = load_price_points_csv(csv_path)
    prices_by_time = group_prices_by_time(points)

    # Group by symbol for Kalman
    symbol_series: dict[str, list[float]] = {}
    for ts in sorted(prices_by_time):
        for sym, price in prices_by_time[ts].items():
            symbol_series.setdefault(sym, []).append(price)

    for sym, prices in symbol_series.items():
        if not prices:
            continue
        kf = StockKalmanFilter(initial_price=prices[0])
        print(f"\n=== {sym} ===")
        for p in prices[1:]:
            pred, filt = kf.step(p)
            print(f"live={p:.2f} | pred={pred:.2f} | filt={filt:.2f}")


if __name__ == "__main__":
    # Example usage - replace with your CSV path
    run_kalman_on_csv("/opt/rubicon/sample_data.csv")
