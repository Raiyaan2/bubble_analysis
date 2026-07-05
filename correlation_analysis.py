import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Load cleaned monthly data
# -----------------------------

data = pd.read_csv("output/monthly_macro_financial_data.csv", parse_dates=["Date"])
data = data.set_index("Date")

# -----------------------------
# 2. Calculate S&P 500 monthly return
# -----------------------------

data["S&P 500 Return"] = data["S&P 500"].pct_change()

# -----------------------------
# 3. Define indicators and periods
# -----------------------------

indicators = [
    "VIX",
    "Leverage Subindex",
    "Bank Tightening Standards"
]

periods = {
    "Dot-com": ("1995-01-01", "2000-03-31"),
    "Housing": ("2002-01-01", "2007-10-31"),
    "Current": ("2022-01-01", "2026-12-31"),
}

# -----------------------------
# 4. Calculate correlations
# -----------------------------

correlation_results = {}

for period_name, (start, end) in periods.items():
    period_data = data.loc[start:end].copy()

    # Keep only S&P return and indicators
    period_data = period_data[["S&P 500 Return"] + indicators]

    # Drop missing values
    period_data = period_data.dropna()

    correlations = {}

    for indicator in indicators:
        corr = period_data["S&P 500 Return"].corr(period_data[indicator])
        correlations[indicator] = corr

    correlation_results[period_name] = correlations

# Convert to table
correlation_table = pd.DataFrame(correlation_results)

print("\nCorrelation between indicators and S&P 500 monthly returns:")
print(correlation_table)

# -----------------------------
# 5. Save results
# -----------------------------

os.makedirs("output", exist_ok=True)

correlation_table.to_csv("output/correlation_results.csv")
correlation_table.to_excel("output/correlation_results.xlsx")

# -----------------------------
# 6. Create bar chart
# -----------------------------

ax = correlation_table.plot(
    kind="bar",
    figsize=(10, 6),
    edgecolor="black"
)

plt.title("Correlation with S&P 500 Monthly Returns", fontsize=14, fontweight="bold")
plt.ylabel("Correlation coefficient")
plt.xlabel("Indicator")
plt.axhline(0, color="black", linewidth=1)
plt.grid(axis="y", alpha=0.3)
plt.legend(title="Period")
plt.tight_layout()

plt.savefig("output/correlation_results.png", dpi=300)
plt.show()

print("\nDone. Correlation results saved in the output folder.")