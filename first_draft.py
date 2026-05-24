import numpy as np
import matplotlib.pyplot as plt

SIMULATIONS = 1000
YEARS = 30

initial_debt_to_gdp = 1.20  # 120% debt to GDP
primary_deficit = 0.05  # Government spends 5% more than tax revenue

#
mean_gdp_growth = 0.02  # 2% average real growth
std_gdp_growth = 0.025  # volatility of growth

mean_interest_rate = 0.03  # 3% avg real interest rate
std_interest_rate = 0.01  # vol of interest rate


debt_matrix = np.zeros((SIMULATIONS, YEARS + 1))
debt_matrix[:, 0] = initial_debt_to_gdp

np.random.seed(42)  # ensure that different numbers get generated with each invoke
for i in range(1, YEARS + 1):
    g = np.random.normal(mean_gdp_growth, std_gdp_growth, SIMULATIONS)
    r = np.random.normal(mean_interest_rate, std_interest_rate, SIMULATIONS)

    # Get T-1 debt level for all simulations
    prev_debt = debt_matrix[:, i - 1]

    ## If a simulation's previous debt exceeds 150% (1.5), markets demand a higher risk premium.
    # We dynamically inject an extra penalty to the interest rate for those specific paths.
    risk_premium = np.where(prev_debt > 1.50, 0.025, 0.0)
    r_adjusted = r + risk_premium

    # Core debt formula
    new_debt = (1 + r_adjusted - g) * prev_debt + primary_deficit
    # debt cannot fall below zero
    debt_matrix[:, i] = np.maximum(new_debt, 0)

final_debt_levels = debt_matrix[:, -1]
failed_runs = np.sum(final_debt_levels > 2.50)
failure_probability = (failed_runs / SIMULATIONS) * 100

print(f"Simulation Complete over {YEARS} years.")
print(
    f"Probability of entering an unsustainable debt spiral (>250% GDP): {failure_probability:.1f}%"
)
print(f"Median Final Debt-to-GDP: {np.median(final_debt_levels)*100:.1f}%")

# ------------------------------------------------------------------
# 4. VISUALIZE THE OUTCOMES
# ------------------------------------------------------------------
plt.figure(figsize=(12, 6))

# Plot all 1,000 paths lightly so we can see the "fan" chart distribution
for i in range(SIMULATIONS):
    # Color code: red if it spiraled out of control, gray if it stayed stable
    color = "red" if final_debt_levels[i] > 2.50 else "gray"
    alpha = 0.1 if color == "gray" else 0.2
    plt.plot(range(YEARS + 1), debt_matrix[i, :] * 100, color=color, alpha=alpha)

# Plot the median timeline as a thick black line to see the central tendency
plt.plot(
    range(YEARS + 1),
    np.median(debt_matrix, axis=0) * 100,
    color="black",
    linewidth=2.5,
    label="Median Path",
)

plt.title("Monte Carlo Simulation: Sovereign Debt Sustainability Projections")
plt.xlabel("Years Into Future")
plt.ylabel("Debt-to-GDP Ratio (%)")
plt.axhline(
    150, color="orange", linestyle="--", label="Risk Premium Trigger Threshold (150%)"
)
plt.axhline(250, color="red", linestyle=":", label="System Collapse Threshold (250%)")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.show()
