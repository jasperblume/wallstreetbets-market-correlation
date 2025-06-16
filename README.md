# Correlating WallStreetBets Activity with Stock Market Behavior

## Overview

Reddit’s r/WallStreetBets (WSB) has evolved into a significant source of retail investor sentiment—often chaotic, occasionally insightful, and sometimes market-moving. This project explores whether metrics like daily mention frequency and sentiment scores from WSB align with actual stock market behavior.

We focus on six tickers with strong fundamentals and frequent WSB attention:

- **NVDA** – NVIDIA Corp  
- **TSLA** – Tesla Inc  
- **SPY** – SPDR S&P 500 ETF  
- **PLTR** – Palantir Technologies Inc  
- **SMCI** – Super Micro Computer Inc  
- **RDDT** – Reddit Inc  

The goal is to assess whether WSB data offers any reliable signals or simply reflects investor reactions.

---

## Research Questions & Summary of Findings

1. **Is WSB discussion consistent over time?**  
   No — mention frequency fluctuates dramatically, often in response to news or earnings cycles.

2. **Do mentions correlate with trading volume?**  
   Yes — higher mention counts are associated with increased trading volume across all tickers.

3. **Do mentions correlate with absolute returns?**  
   Yes — greater attention tends to coincide with larger (positive or negative) price movements.

4. **Does sentiment correlate with price direction?**  
   Barely — while some correlations are statistically significant, they are too weak to be predictive.

5. **Does sentiment lead or lag market activity?**  
   Lag — sentiment mostly trails price movement, suggesting users are reacting to market events.

---

## Methods and Tools

- Statistical analysis was conducted using `scipy.stats.pearsonr`
- Bonferroni correction was applied to control for multiple comparisons across six tickers
- Each research question followed a structured hypothesis testing framework
- Sentiment and mention data were pulled using QuantConnect’s QuiverQuant integration
- Historical stock data came from the `yfinance` API

---

## Setup Instructions

### Option 1: Use Preprocessed Data (Recommended)

Data has already been cleaned and merged:
1. Download the dataset from  
   [Google Drive](https://drive.google.com/drive/folders/1m9k6t0E2MoKqeiMhOwU9962Bk2SkoP9R?usp=drive_link)
2. Upload the files to your working environment
3. Update any file paths in your code if needed
4. Run the analysis sections as-is

### Option 2: Pull Raw Data via API (QuantConnect users)

Requires Lean CLI + QuantConnect credentials:
~~~bash
pip install lean yfinance
lean init
lean create-project "WSB-Analysis"
lean data download --dataset "WallStreetBets" --ticker "NVDA,TSLA,SPY,PLTR,SMCI,RDDT"
~~~

---

## Data Sources

- **QuiverQuant (via QuantConnect)** — WSB mentions, sentiment scores, and rankings by ticker  
- **Yahoo Finance (`yfinance`)** — Daily close prices and trading volumes for each stock

---

## Processing Workflow

1. Create a continuous trading calendar from 2018–2025  
2. Merge Reddit data (fill missing dates with zeros, normalize sentiment)  
3. Join with daily price and volume data  
4. Calculate absolute and percentage returns  
5. Perform correlation and lead-lag analysis by ticker

---

## Dependencies

~~~python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
from scipy import stats
import os
~~~

---

## References

- [yfinance Documentation](https://ranaroussi.github.io/yfinance/)  
- [scipy.stats.pearsonr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html)  
- [pandas.DataFrame.shift](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html)  
- [seaborn.regplot](https://seaborn.pydata.org/generated/seaborn.regplot.html)  
- [Colab File Downloads](https://stackoverflow.com/questions/48774285/how-to-download-file-created-in-colaboratory-workspace)

---
