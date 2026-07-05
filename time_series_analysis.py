import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf

# -----------------------------
# 1. Settings
# -----------------------------

START_DATE = "1995-01-01"
END_DATE = "2026-12-31"

periods = {
    "Dot-com Bubble": ("1995-01-01", "2000-03-31"),
    "Housing Bubble": ("2002-01-01", "2007-10-31"),
    "Current Market": ("2022-01-01", "2026-12-31"),
}

period_colors = {
    "Dot-com Bubble": "#44688a",
    "Housing Bubble": "#479147",
    "Current Market": "#cf4634",
}

fred_series = {
    "VIX": "VIXCLS",
    "Leverage Subindex": "NFCILEVERAGE",
    "Bank Tightening Standards": "DRTSCIS",
}

os.makedirs("output", exist_ok=True)

# -----------------------------
# 2. Download data
# -----------------------------

print("Downloading S&P 500 from Yahoo Finance...")
sp500 = yf.download("^GSPC", start=START_DATE, end=END_DATE, progress=False)

if isinstance(sp500.columns, pd.MultiIndex):
    sp500_close = sp500["Close"].iloc[:, 0]
else:
    sp500_close = sp500["Close"]

sp500_close.name = "S&P 500"

data = pd.DataFrame(sp500_close)

for name, fred_id in fred_series.items():
    print(f"Downloading {name} from FRED...")
    data[name] = pdr.DataReader(fred_id, "fred", START_DATE, END_DATE)

# -----------------------------
# 3. Convert to monthly data
# -----------------------------

monthly = data.resample("ME").mean()
monthly["Bank Tightening Standards"] = monthly["Bank Tightening Standards"].ffill()

monthly = monthly.dropna(subset=["S&P 500"])

monthly.to_csv("output/monthly_macro_financial_data.csv")
monthly.to_excel("output/monthly_macro_financial_data.xlsx")

# -----------------------------
# 4. Function to plot S&P 500 vs one indicator
# -----------------------------

def plot_indicator(indicator, file_name, indicator_label):
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Highlight periods
    for period_name, (start, end) in periods.items():
        ax1.axvspan(
            pd.to_datetime(start),
            pd.to_datetime(end),
            color=period_colors[period_name],
            alpha=0.35,
            label=period_name,
        )

    # S&P 500 left axis
    ax1.plot(
        monthly.index,
        monthly["S&P 500"],
        color="#0b3d91",
        linewidth=2,
        label="S&P 500",
    )
    ax1.set_ylabel("S&P 500 Index Level", color="#0b3d91")
    ax1.tick_params(axis="y", labelcolor="#0b3d91")

    # Indicator right axis
    ax2 = ax1.twinx()
    ax2.plot(
        monthly.index,
        monthly[indicator],
        color="#d62728",
        linewidth=2,
        label=indicator_label,
    )
    ax2.set_ylabel(indicator_label, color="#d62728")
    ax2.tick_params(axis="y", labelcolor="#d62728")

    plt.title(f"S&P 500 vs {indicator_label} (1995–2026)", fontsize=15, fontweight="bold")

    ax1.set_xlabel("Date")
    ax1.grid(True, alpha=0.3)

    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

    fig.text(
        0.5,
        0.01,
        "Shaded areas: Dot-com Bubble (1995–2000), Housing Bubble (2002–2007), Current Market (2022–latest). Sources: Yahoo Finance and FRED.",
        ha="center",
        fontsize=9,
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(f"output/{file_name}", dpi=300)
    plt.show()

# -----------------------------
# 5. Create three graphs
# -----------------------------

plot_indicator("VIX", "sp500_vs_vix.png", "VIX")
plot_indicator("Leverage Subindex", "sp500_vs_leverage_subindex.png", "Chicago Fed Leverage Subindex")
plot_indicator("Bank Tightening Standards", "sp500_vs_bank_tightening_standards.png", "SLOOS Bank Tightening Standards")

print("Done. Three graphs saved in the output folder.")