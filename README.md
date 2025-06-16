# WallStreetBets Market Correlation Analysis

Statistical analysis examining the relationship between r/WallStreetBets discussion patterns and stock market behavior across 6 major securities (NVDA, TSLA, SPY, PLTR, SMCI, RDDT).

## Key Findings

- **Strong correlation** between WSB mentions and trading volume (r=0.14-0.71, all p<0.001)
- **Moderate correlation** between mentions and price volatility (r=0.21-0.46, all p<0.001)  
- **Minimal predictive value** from sentiment analysis (r≤0.12)
- **WSB primarily reacts to** rather than predicts market movements

## Quick Start

```bash
git clone https://github.com/yourusername/wallstreetbets-market-correlation.git
cd wallstreetbets-market-correlation
pip install -r requirements.txt
jupyter notebook main_analysis.ipynb
```

## What's Included

- **Complete dataset** (Aug 2018 - Feb 2025) with WSB mentions, sentiment scores, and market data
- **5 research questions** with statistical hypothesis testing
- **Correlation analysis** using Bonferroni correction for multiple comparisons
- **Lead/lag analysis** examining temporal relationships
- **Reproducible results** with modular functions

## Research Questions

1. Is WSB discussion consistent over time?
2. Do mentions correlate with trading volume?
3. Do mentions correlate with price volatility?
4. Does sentiment predict price direction?
5. Do WSB users lead or lag market movements?

## Dependencies

- pandas, numpy, matplotlib, seaborn
- scipy (statistical testing)
- yfinance (market data)

## Data Sources

- **WSB data**: QuantConnect/Quiver Quantitative
- **Market data**: Yahoo Finance
- **Coverage**: 5 stocks over 6.5 years (2,400+ trading days)

## Authors
Jasper Blume, Eli Haas, Ian Chiu

---
_This analysis demonstrates that while WSB discussion volume reliably indicates market attention and volatility, sentiment provides negligible predictive value for price direction._
