"""Configuration for local data setup."""
import os

# Analysis settings
STOCK_TICKERS = ["NVDA", "TSLA", "SPY", "PLTR", "SMCI", "RDDT"]
START_DATE = '2018-08-01'
END_DATE = '2025-02-21'

# Bonferroni correction settings
ALPHA = 0.05  
NUM_COMPARISONS = len(STOCK_TICKERS) 
BONFERRONI_THRESHOLD = ALPHA / NUM_COMPARISONS 

# Local data paths (relative to project root)
DATA_DIR = "data"
RAW_WSB_DIR = os.path.join(DATA_DIR, "raw_wsb")
RAW_YFINANCE_DIR = os.path.join(DATA_DIR, "raw_yfinance") 
MERGED_DIR = os.path.join(DATA_DIR, "merged")
