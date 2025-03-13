"""Module Description:
    This module downloads, cleans, and processes QQQM holdings data from Invesco and merges it with stock quotes.
    It includes caching and error handling logic.
"""
import requests
import pandas as pd
from io import BytesIO

from src.xueqiu_data import getBatchQuote
# Adding cache variable
_ndx_holding_cache = None

def downloadQQQMHolding():
    """
    Downloads the QQQM holdings data from Invesco and caches it.
    Returns the dataframe containing the holdings data.
    """
    global _ndx_holding_cache
    if _ndx_holding_cache is not None:
        return _ndx_holding_cache

    try:
        # Send a GET request to the URL
        url = "https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=QQQM"  
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Use BytesIO to convert byte content into a file object
        content_io = BytesIO(response.content)
        # Use pandas to read CSV content
        df = pd.read_csv(content_io)
        _ndx_holding_cache = df  # Cache the data
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the CSV file: {e}")

# Clean up the dataframe
def getQQQMHolding():
    """
    Cleans and processes the downloaded QQQM holdings data, merges it with stock quotes, and returns the final dataframe.
    In case of failure, loads the local cached data.
    """
    try:
        df = downloadQQQMHolding()
        df = df.rename(columns={'Holding Ticker': 'Ticker'})
        df['Ticker'] = df['Ticker'].str.strip()

        valid_classes = ['Common Stock', 'American Depository Receipt', 'American Depository Receipt - NY']
        df = df[df['Class of Shares'].isin(valid_classes)]

        filter_column = ['Ticker', 'Name', 'Weight', 'Sector', 'Class of Shares']
        df = df[filter_column]

        # Convert the 'Weight' column to numeric type
        df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
        df["Weight"] = df["Weight"] / df["Weight"].sum()

        xueqiu_df = getBatchQuote(df['Ticker'])

        # Merge on the 'Ticker' column
        merged_df = pd.merge(df, xueqiu_df, left_on='Ticker', right_on='symbol')
        
        # Sorting

        merged_df = merged_df.rename(columns={
            'current': 'Price',
            'percent': 'IntradayReturn',
            'exchange': 'Exchange',
            'volume': 'Volume',
            'amount': 'Amount',
            'market_capital': 'MarketCap',
            'current_year_percent': 'YTDReturn',
            'total_shares': 'SharesOutstanding',
            'pe_ttm': 'PE',
            'pe_forecast': 'ForwardPE',
            'pb': 'PB',
            'dividend': 'Dividend',
            'dividend_yield': 'DividendYield',
            'profit_four': 'Profit_TTM',
            'Timestamp_str': 'Date',
        })
        merged_df['IntradayContribution'] = merged_df['Weight'] * merged_df['IntradayReturn']
        merged_df['YTDContribution'] = merged_df['Weight'] * merged_df['YTDReturn']

        output_columns = ['Ticker', 'Name', 'Weight', 'Price', 'IntradayReturn',
                          'Volume', 'Amount', 'IntradayContribution',
                          'MarketCap', 'YTDReturn', 'YTDContribution',
                          'PE', 'PB', 'Profit_TTM', 'DividendYield', 'Dividend',
                          'SharesOutstanding', 'Sector', 'Date']
        merged_df = merged_df[output_columns]
    except:
        print("Network issue detected.")
        merged_df = pd.read_csv("data/raw/QQQM_Data.csv")

    return merged_df

    
if __name__ == "__main__":
    df = getQQQMHolding()
    print(df)

