import pytest
import pandas as pd
from src.xueqiu_data import getBatchQuote

def test_getBatchQuote_returns_data():
    """Test that getBatchQuote returns a non-empty DataFrame for provided tickers."""
    stock_ticker_list = ['AAPL', 'GOOG']
    df = getBatchQuote(stock_ticker_list)
    assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame."
    assert not df.empty, "DataFrame should not be empty."

from src.xueqiu_data import getUSStockHistoryByDate

def test_getUSStockHistoryByDate_returns_data():
    """Test that getUSStockHistoryByDate returns a non-empty DataFrame with the correct ticker for symbol 'GOOGL' and start_date '2025-02-03'."""
    df = getUSStockHistoryByDate(symbol='GOOGL', start_date='2025-02-03')
    assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame."
    assert not df.empty, "DataFrame should not be empty."
    # Check if the Ticker column exists and all rows have the value 'GOOGL'
    assert 'Ticker' in df.columns, "DataFrame should contain a 'Ticker' column."
    assert all(df['Ticker'] == 'GOOGL'), "All Ticker values should be 'GOOGL'."
