"""Utility functions with local file paths."""
import pandas as pd
import numpy as np
import os
import yfinance as yf
from config import *

def download_yfinance_data(start_date=START_DATE, end_date=END_DATE, tickers=STOCK_TICKERS):
    """Download data to local directory instead of Google Drive."""
    os.makedirs(RAW_YFINANCE_DIR, exist_ok=True)
    downloaded_files = []
    
    for ticker in tickers:
        dat = yf.Ticker(ticker)
        ticker_data = dat.history(start=start_date, end=end_date)
        file_name = f"yfinancedata_{ticker}.csv"
        file_path = os.path.join(RAW_YFINANCE_DIR, file_name)
        ticker_data.to_csv(file_path, index=True)
        downloaded_files.append(file_name)
        print(f"Saved {ticker} to {file_path}")
    
    return downloaded_files

def clean_data_yfinance_WSB(start_date=START_DATE, end_date=END_DATE):
    """Clean and merge data using local paths."""
    os.makedirs(MERGED_DIR, exist_ok=True)
    
    yfinance_files = os.listdir(RAW_YFINANCE_DIR)
    saved_files = []
    
    for file_yfinance in yfinance_files:
        if not file_yfinance.endswith('.csv'):
            continue
            
        # Create date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        result_df = pd.DataFrame({'Date': date_range})
        
        # Extract ticker name
        ticker = file_yfinance.split('_')[-1].replace('.csv', '')
        
        # Load WSB data
        wsb_file = os.path.join(RAW_WSB_DIR, f"{ticker.lower()}.csv")
        yfinance_file = os.path.join(RAW_YFINANCE_DIR, file_yfinance)
        
        if not os.path.exists(wsb_file):
            print(f"Warning: WSB file not found for {ticker}")
            continue
            
        # Load and process data
        yfinance_df = pd.read_csv(yfinance_file).copy()
        wsb_df = pd.read_csv(wsb_file, header=None).copy()
        wsb_df.columns = ["Date", "Mention_Count", "Mention_Rank", "Sentiment_Score"]
        
        # Convert dates
        yfinance_df["Date"] = pd.to_datetime(yfinance_df["Date"], utc=True).dt.date
        wsb_df["Date"] = pd.to_datetime(wsb_df["Date"], format="%Y%m%d").dt.date
        result_df["Date"] = pd.to_datetime(result_df["Date"], utc=True).dt.date
        
        # Merge data
        result_df = pd.merge(result_df, wsb_df, on='Date', how='left')
        result_df = result_df.fillna(0)
        result_df = pd.merge(result_df, yfinance_df[["Date", "Close", "Volume"]], on='Date', how='left')
        
        # Save merged file
        output_file = f"{ticker}_merged.csv"
        output_path = os.path.join(MERGED_DIR, output_file)
        result_df.to_csv(output_path, index=False)
        saved_files.append(output_file)
        print(f"Created {output_path}")
    
    return saved_files

def load_ticker_data(tickers=STOCK_TICKERS):
    """Load ticker data from local merged files."""
    ticker_data = {}
    
    for ticker in tickers:
        file_path = os.path.join(MERGED_DIR, f"{ticker}_merged.csv")
        if os.path.exists(file_path):
            ticker_data[ticker] = pd.read_csv(file_path)
            ticker_data[ticker]['Date'] = pd.to_datetime(ticker_data[ticker]['Date'])
            print(f"Loaded {ticker}")
        else:
            print(f"Warning: {file_path} not found")
    
    return ticker_data
