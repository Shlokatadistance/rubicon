from datetime import datetime

from basket import BasketConstituent, HistoricalBasketPricer
from historical_compare import compare_to_reference


def ts(value: str) -> datetime:
    return datetime.fromisoformat(value)


if __name__ == "__main__":
    constituents = [
        BasketConstituent(symbol="US_STOCK", quantity=2.0),
        BasketConstituent(symbol="JP_STOCK", quantity=1.5, fx_rate=0.0068),
    ]

    initial_prices = {
        "US_STOCK": 100.0,
        "JP_STOCK": 3000.0,
    }

    historical_prices = {
        ts("2026-01-01T09:30:00"): {"US_STOCK": 100.0},
        ts("2026-01-01T09:31:00"): {"US_STOCK": 100.4},
        ts("2026-01-01T09:32:00"): {"US_STOCK": 100.2},
        ts("2026-01-01T09:33:00"): {"JP_STOCK": 3010.0},
        ts("2026-01-01T09:34:00"): {"US_STOCK": 100.8},
    }

    reference_prices = {
        ts("2026-01-01T09:30:00"): 230.60,
        ts("2026-01-01T09:31:00"): 231.10,
        ts("2026-01-01T09:32:00"): 230.90,
        ts("2026-01-01T09:33:00"): 231.20,
        ts("2026-01-01T09:34:00"): 232.00,
    }

    pricer = HistoricalBasketPricer(
        constituents=constituents,
        initial_prices=initial_prices,
        price_noise=0.25,
        volatility=0.02,
    )

    snapshots = pricer.run(historical_prices)
    comparisons = compare_to_reference(snapshots, reference_prices)

    for comparison in comparisons:
        print(
            comparison.timestamp.isoformat(),
            f"basket={comparison.basket_price:.2f}",
            f"reference={comparison.reference_price:.2f}",
            f"diff={comparison.difference:.2f}",
            f"diff_pct={comparison.percentage_difference:.2%}",
        )
