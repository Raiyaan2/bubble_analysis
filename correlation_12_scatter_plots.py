import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 1. Load monthly data
# -----------------------------

data = pd.read_csv("output/monthly_macro_financial_data.csv")

if "Date" in data.columns:
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.set_index("Date")
elif "DATE" in data.columns:
    data["DATE"] = pd.to_datetime(data["DATE"])
    data = data.set_index("DATE")

# -----------------------------
# 2. Calculate S&P 500 monthly return
# -----------------------------

data["S&P 500 Return"] = data["S&P 500"].pct_change()

# -----------------------------
# 3. Settings
# -----------------------------

periods = {
    "dot_com": {
        "label": "Dot-com Bubble (1995-2000)",
        "start": "1995-01-01",
        "end": "2000-03-31",
        "color": "#44688a",
    },
    "housing": {
        "label": "Housing Bubble (2002-2007)",
        "start": "2002-01-01",
        "end": "2007-10-31",
        "color": "#479147",
    },
    "current": {
        "label": "Current Market (2022-latest)",
        "start": "2022-01-01",
        "end": "2026-12-31",
        "color": "#cf4634",
    },
}

indicators = {
    "sp500": {
        "column": "S&P 500",
        "label": "S&P 500 Index Level",
    },
    "vix": {
        "column": "VIX",
        "label": "VIX",
    },
    "leverage_subindex": {
        "column": "Leverage Subindex",
        "label": "Chicago Fed Leverage Subindex",
    },
    "bank_tightening_standards": {
        "column": "Bank Tightening Standards",
        "label": "SLOOS Bank Tightening Standards",
    },
}

os.makedirs("output/correlation_scatter_plots", exist_ok=True)

# -----------------------------
# 4. Create one scatter plot per indicator and period
# -----------------------------

summary_rows = []

for indicator_key, indicator_info in indicators.items():
    indicator_col = indicator_info["column"]
    indicator_label = indicator_info["label"]

    for period_key, period_info in periods.items():
        period_label = period_info["label"]
        start = period_info["start"]
        end = period_info["end"]
        color = period_info["color"]

        period_data = data.loc[start:end, [indicator_col, "S&P 500 Return"]].dropna()

        if period_data.empty or len(period_data) < 3:
            print(f"Skipping {indicator_label} - {period_label}: not enough data.")
            continue

        x = period_data[indicator_col]
        y = period_data["S&P 500 Return"]

        r = x.corr(y)

        slope, intercept = np.polyfit(x, y, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept

        plt.figure(figsize=(8, 6))

        plt.scatter(
            x,
            y,
            color=color,
            alpha=0.75,
            edgecolor="black",
            linewidth=0.4,
        )

        plt.plot(
            x_line,
            y_line,
            color=color,
            linewidth=2.5,
        )

        plt.title(
            f"{indicator_label} vs S&P 500 Monthly Return\n{period_label}",
            fontsize=13,
            fontweight="bold",
        )

        plt.xlabel(indicator_label)
        plt.ylabel("S&P 500 Monthly Return")
        plt.grid(True, alpha=0.3)

        plt.text(
            0.05,
            0.90,
            f"R = {r:.2f}",
            transform=plt.gca().transAxes,
            fontsize=12,
            bbox=dict(facecolor="white", edgecolor="black", alpha=0.85),
        )

        plt.figtext(
            0.5,
            0.01,
            "Each point represents one month. The line shows the linear best fit. R = Pearson correlation coefficient.",
            ha="center",
            fontsize=9,
        )

        plt.tight_layout(rect=[0, 0.04, 1, 1])

        file_name = f"{period_key}_{indicator_key}_correlation.png"
        file_path = f"output/correlation_scatter_plots/{file_name}"

        plt.savefig(file_path, dpi=300)
        plt.close()

        summary_rows.append({
            "Period": period_label,
            "Indicator": indicator_label,
            "Correlation_R": r,
            "Slope": slope,
            "Observations": len(period_data),
            "File": file_name,
        })

        print(f"Saved: {file_path}")

# -----------------------------
# 5. Save summary table
# -----------------------------

summary = pd.DataFrame(summary_rows)
summary.to_csv("output/correlation_scatter_plots/correlation_summary.csv", index=False)
summary.to_excel("output/correlation_scatter_plots/correlation_summary.xlsx", index=False)

print("Done. 12 correlation scatter plots saved in output/correlation_scatter_plots.")