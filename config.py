"""Configuration for local data setup."""
import os

# Analysis settings
STOCK_TICKERS = ["NVDA", "TSLA", "SPY", "PLTR", "SMCI", "RDDT"]
START_DATE = '2018-08-01'
END_DATE = '2025-02-21'
BONFERRONI_THRESHOLD = 0.0083

# Local data paths (relative to project root)
DATA_DIR = "data"
RAW_WSB_DIR = os.path.join(DATA_DIR, "raw_wsb")
RAW_YFINANCE_DIR = os.path.join(DATA_DIR, "raw_yfinance") 
MERGED_DIR = os.path.join(DATA_DIR, "merged")
