"""Core analysis functions for WSB research questions."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from config import BONFERRONI_THRESHOLD, STOCK_TICKERS

def calculate_pct_change_close(ticker_data):
    """Calculate percent daily changes (decimal) for Close price."""
    ticker_data['Pct_Change_Close'] = ticker_data['Close'].pct_change()
    return ticker_data

def create_shifted_data(original_data, shift_days):
    """
    Creates a new dictionary with shifted sentiment metrics
    Parameters:
    - original_data: Dictionary with ticker:dataframe pairs
    - shift_days: Number of days to shift (negative for lead, positive for lag)
    Returns:
    - Dictionary with shifted data and NaNs removed
    """
    columns_to_shift = ['Mention_Count', 'Mention_Rank', 'Sentiment_Score']
    result = {}
    for ticker, data in original_data.items():
        shifted_data = data.copy()
        shifted_data[columns_to_shift] = shifted_data[columns_to_shift].shift(shift_days)
        result[ticker] = shifted_data.dropna()
    return result

def plot_mentions(ticker_data):
    """
    Plot mentions over time for each ticker and return the ax object.
    Parameters:
    ticker_data (dict): Dictionary with ticker symbols as keys and DataFrames as values
    Returns:
    matplotlib.axes: The plot's axes object
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker, df in ticker_data.items():
        sns.lineplot(x='Date', y='Mention_Count', data=df, label=ticker, ax=ax)
    ax.set_title('WSB Mentions Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Mention Count')
    plt.xticks(rotation=45)
    plt.legend()
    return ax

def analyze_mention_volume_correlation(df, ax=None, ticker=""):
    """
    Correlation analysis between mention count and trading volume.
    Parameters:
    - df: DataFrame for a specific ticker
    - ax: Matplotlib axis to plot on
    - ticker: Ticker symbol to include in the title
    Returns:
    - r: Pearson correlation coefficient
    - p: p-value for the correlation
    """
    valid_data = df.dropna(subset=['Mention_Count', 'Volume'])
    r, p = stats.pearsonr(valid_data['Mention_Count'], valid_data['Volume'])
    
    if ax is not None:
        sns.regplot(x='Mention_Count', y='Volume', data=valid_data, ax=ax)
        ax.set_title(f'{ticker}: Mentions vs Volume (r={r:.3f}, p={p:.3f})')
        ax.set_xlabel('Mention Count')
        ax.set_ylabel('Trading Volume')
    
    return r, p

def analyze_mention_abs_price_correlation(df, ax=None, ticker=""):
    """
    Correlation analysis between mention count and absolute percentage price changes.
    Parameters:
    - df: DataFrame for a specific ticker
    - ax: Matplotlib axis to plot on
    - ticker: Ticker symbol to include in the title
    Returns:
    - r: Pearson correlation coefficient
    - p: p-value for the correlation
    """
    valid_data = df.dropna().copy()
    valid_data['Abs_Pct_Change'] = np.abs(valid_data['Pct_Change_Close'])
    r, p = stats.pearsonr(valid_data['Mention_Count'], valid_data['Abs_Pct_Change'])
    
    if ax is not None:
        sns.regplot(x='Mention_Count', y='Abs_Pct_Change', data=valid_data, ax=ax)
        ax.set_title(f'{ticker}: Mentions vs |Price Change %| (r={r:.3f}, p={p:.3f})')
        ax.set_xlabel('Mention Count')
        ax.set_ylabel('Absolute Percentage Price Change')
    
    return r, p

def analyze_sentiment_price_correlation(df, ax=None, ticker=""):
    """
    Correlation analysis between sentiment and percentage price changes.
    Parameters:
    - df: DataFrame for a specific ticker
    - ax: Matplotlib axis to plot on
    - ticker: Ticker symbol to include in the title
    Returns:
    - r: Pearson correlation coefficient
    - p: p-value for the correlation
    """
    valid_data = df.dropna(subset=['Sentiment_Score', 'Pct_Change_Close'])
    r, p = stats.pearsonr(valid_data['Sentiment_Score'], valid_data['Pct_Change_Close'])
    
    if ax is not None:
        sns.regplot(x='Sentiment_Score', y='Pct_Change_Close', data=valid_data, ax=ax)
        ax.set_title(f'{ticker}: Sentiment vs Price Change % (r={r:.3f}, p={p:.3f})')
        ax.set_xlabel('Sentiment Score')
        ax.set_ylabel('Percentage Price Change')
    
    return r, p

def calculate_lead_lag_indicator(correlations):
    """
    Calculate a simple lead/lag indicator.
    Parameters:
    - correlations: List of correlation values for all shifts [lag_3, lag_2, lag_1, 0, lead_1, lead_2, lead_3]
    Returns:
    - indicator: The lead/lag indicator value (positive = leading, negative = lagging)
    """
    lag_mean = sum(correlations[0:3]) / 3   # lag_3, lag_2, lag_1
    lead_mean = sum(correlations[4:7]) / 3  # lead_1, lead_2, lead_3
    return lead_mean - lag_mean

def analyze_lead_lag_correlations(ticker, ax, lead_lag_data):
    """
    Create a bar plot showing correlations between sentiment and price changes
    across different lead and lag periods.
    Parameters:
    - ticker: Ticker symbol to analyze
    - ax: Matplotlib axis to plot on
    - lead_lag_data: Dict with keys like 'lead_3', 'lead_2', etc., each containing ticker data
    Returns:
    - indicator: The lead/lag indicator value
    - zero_correlation: The correlation at time shift 0
    """
    shifts = ["lag_3", "lag_2", "lag_1", "0", "lead_1", "lead_2", "lead_3"]
    correlations = []
    
    for shift in shifts:
        shift_df = lead_lag_data[shift][ticker]
        valid_data = shift_df.dropna(subset=['Sentiment_Score', 'Pct_Change_Close'])
        if len(valid_data) >= 3:
            r, p = stats.pearsonr(valid_data['Sentiment_Score'], valid_data['Pct_Change_Close'])
            correlations.append(r)
        else:
            correlations.append(0)
    
    ax.bar(shifts, correlations)
    ax.axhline(y=0, color='black', linestyle='-')
    indicator = calculate_lead_lag_indicator(correlations)
    ax.set_title(f'{ticker}: Lead-Lag Indicator: {indicator:.3f}')
    ax.set_xlabel('Time Shift')
    ax.set_ylabel('Correlation')
    
    zero_correlation = correlations[3]
    return indicator, zero_correlation

def run_all_correlations(ticker_data):
    """Run all correlation analyses and return summary results."""
    results = {}
    
    for ticker, df in ticker_data.items():
        r1, p1 = analyze_mention_volume_correlation(df)
        r2, p2 = analyze_mention_abs_price_correlation(df)
        r3, p3 = analyze_sentiment_price_correlation(df)
        
        results[ticker] = {
            'mention_volume_r': r1, 'mention_volume_p': p1,
            'mention_abs_price_r': r2, 'mention_abs_price_p': p2,
            'sentiment_price_r': r3, 'sentiment_price_p': p3,
            'significant_bonferroni': [p1 < BONFERRONI_THRESHOLD, 
                                     p2 < BONFERRONI_THRESHOLD, 
                                     p3 < BONFERRONI_THRESHOLD]
        }
    
    return results
