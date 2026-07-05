# Bubble Analysis Project

This project analyses the relationship between macro-financial indicators and S&P 500 performance during:

- Dot-com Bubble
- Housing Bubble
- Current Market

## Indicators Used

- VIX
- Chicago Fed NFCI Leverage Subindex
- SLOOS Bank Tightening Standards
- S&P 500

## Setup Instructions

### 1. Clone this repository

```bash
git clone <repository-link>
cd bubble_analysis
```

## Python Files

### `time_series_analysis.py`
Downloads S&P 500 data from Yahoo Finance and macro-financial indicators from FRED.  
It creates time-series graphs comparing the S&P 500 with each indicator from 1995 to the latest available data.

### `correlation_analysis.py`
Calculates the Pearson correlation between each indicator and monthly S&P 500 returns for each period:
- Dot-com Bubble
- Housing Bubble
- Current Market

It outputs a correlation table.

### `correlation_12_scatter_plots.py`
Creates separate scatter plots for each indicator and each period.  
Each chart includes:
- Monthly observations
- Line of best fit
- Pearson correlation coefficient (R)

The output files are saved in:

```bash
output/correlation_scatter_plots/
