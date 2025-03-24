"""This module is used to fetch and process stock data from the Xueqiu API,
including batch quote data and historical US stock data, as well as perform time conversion and data calculations.

Main functions:
    - getBatchQuote: Fetches batch stock quotes and returns a DataFrame.
    - get_current_beijing_time: Returns the current Beijing time in milliseconds.
    - get_current_newyork_time: Returns the current New York time in milliseconds.
    - calculate_date_difference: Calculates the difference in days between the current date and a specified date.
    - getUSStockHistoryByDate: Fetches historical US stock data within a given date range and computes moving averages.
"""

import requests
import pandas as pd
from datetime import datetime
import pytz

import requests


# Extract headers
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,et;q=0.7',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

# Extract cookies
cookies = {
    'cookiesu': '501716971730603',
    'device_id': 'b466cc5fe5c41c2cf5113e1dc9758e94',
    's': 'br1biz2pdb',
    'bid': '3f1caaa1da9c9048cf5319e6a0c33666_lwsmxccn',
    'xq_is_login': '1',
    'u': '2110750062',
    'xq_a_token': 'ad394ced1eb5707d9926b7342d2aae0c4c6d5762',
    'xqat': 'ad394ced1eb5707d9926b7342d2aae0c4c6d5762',
    'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxMTA3NTAwNjIsImlzcyI6InVjIiwiZXhwIjoxNzQ1MzY2ODMwLCJjdG0iOjE3NDI3NzQ4MzA0MDUsImNpZCI6ImQ5ZDBuNEFadXAifQ.Z-mGI_SUS8ZLs-ULLPuS4e57ToxuJtvr_ACqW3H4vhru_chjYnmOeYPL_fq9vtRWZlPICumWoDSasmCK97PlgB4UaBSMJT5yiJYIKgsBH7aNC3mPU4iI9kiN-PzS78tLhtz4n6VAnZvmWust--LUWRVX3bNLnSVpMrmuEx2yPq23ism4d5-TirYoNxiZ8k7yhANciEuEx64k__VQfsCFvOqnnF387X38WASsT_phDJNpkT5aDaLXAlQsh4oKpdCt1tiy6IZMqSwLN3F4ci_o1XJKjFdGh-G6-GX87D8dT317bW1iYOmQSUSJEKITE_H4uQyrm2leyEjwoRPCC0QoPg',
    'xq_r_token': '3b737bccb2dc7fde2bd8bd9c1a3835a305eede31',
    'is_overseas': '1',
    'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1742512425,1742534199,1742575630,1742774972',
    'HMACCOUNT': '90AC0DA1311E6AC3',
    'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1742774975',
    'ssxmod_itna': 'eq0xuDRDyD0DgDjxhDh=CD8GtwRDewxq0dGMD3Mq7tDRDFqAPeDHAxfh1CixkhyExxQmi7T5D/K7eGzDiqKGhDBnAzQnxEh6xHbU02D1=WCQ4wmwNf0hwwvNXMrOowiQ40aDbqGkoKg5GGm4GwDGoD34DiDDPDb8NDAMeD7qDFblrovCrDm4GWbeGfDDoDY32xxit3DDUIRqG2WhrKDDNK0pxDaGD4D6nlbZe7hnGbg3rDjTPD/RKIOYrFk/OKUjWwgRuwKeGySKGuIleQyq9O7QT3ZjtQt4xbU4x4K2ImQAGQ70DYY+Dkn0K/vlQDKWD4K0qtGtK2a4uaDDWVrz=j3qD4w0khkCpMCwGzPg177DXMYiGD52Y1DxiGx9BmLEz+E53B5G2ph2KjEs5nK9hx4D',
    'ssxmod_itna2': 'eq0xuDRDyD0DgDjxhDh=CD8GtwRDewxq0dGMD3Mq7tDRDFqAPeDHAxfh1CixkhyExxQmi7keDAKr7GbQeDjRDeiH4GNKNh=BE4eapZeLuxsyfpLIRhw+hQ96el4u08qe/4oMFvs2eZo4QDh8tleKQlP13lmxtm7WY7Y+uPPW5FcFqGp=UZvxTIoWDp7hd2BG0Dh7d99H9jY4kcYENpyp8xp7TKLzn1MWSgy6qm5QFtE=Opl0D/m=7l7Ru4w0b/PWdNEpbtRWe0GtktGsKnxGel=Ik2ogIqh4wQ4BuN+rMnw4VBGIC3XVQ2eKYD'
}


def getBatchQuote(symbols):
    """
    Fetches batch stock quote data for the given symbols from the Xueqiu API and processes it into a DataFrame.
    
    Parameters:
        symbols (list): A list of stock symbol strings.
        
    Returns:
        DataFrame: A pandas DataFrame containing the stock quote data with processed timestamps and scaled percentages.
    """
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]

    # Convert all quote data into DataFrame, with each quote data occupying one row
    df = pd.DataFrame(quote_data_list)
    """
    output_colnames=['symbol', 'code', 'exchange', 'name', 'type', 'sub_type', 'status',
       'current', 'currency', 'percent', 'chg', 'timestamp', 'time',
       'lot_size', 'tick_size', 'open', 'last_close', 'high', 'low',
       'avg_price', 'volume', 'amount', 'turnover_rate', 'amplitude',
       'market_capital', 'float_market_capital', 'total_shares',
       'float_shares', 'issue_date', 'lock_set', 'current_year_percent',
       'high52w', 'low52w', 'variable_tick_size', 'volume_ratio', 'eps',
       'pe_ttm', 'pe_lyr', 'navps', 'pb', 'dividend', 'dividend_yield', 'psr',
       'short_ratio', 'inst_hld', 'beta', 'timestamp_ext', 'current_ext',
       'percent_ext', 'chg_ext', 'contract_size', 'pe_forecast',
       'profit_forecast', 'profit', 'profit_four', 'pledge_ratio',
       'goodwill_in_net_assets', 'shareholder_funds']
    """
    # Convert timestamp to pandas datetime object
    df['Timestamp_str'] = (
        pd.to_datetime(df['timestamp'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('America/New_York')
        .strftime('%Y-%m-%d %H:%M:%S %z')
    )

    # Fill missing values
    df.fillna({'dividend': 0, 'dividend_yield': 0}, inplace=True)

    df['percent'] = df['percent'].div(100)
    df['current_year_percent'] = df['current_year_percent'].div(100)
    try:
        df['dividend_yield'] = df['dividend_yield'].div(100)
    except:
        pass
    
    return df

def get_current_beijing_time():
    """
    Returns the current Beijing time as a timestamp in milliseconds.
    
    Returns:
        int: The current Beijing time in milliseconds.
    """
    # Get current UTC time
    utc_now = datetime.now(pytz.utc)
    # Convert UTC time to Beijing time
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_now = utc_now.astimezone(beijing_tz)
    # Convert Beijing time to milliseconds timestamp
    milliseconds = int(beijing_now.timestamp() * 1000)
    return milliseconds

def get_current_newyork_time():
    """
    Returns the current New York time as a timestamp in milliseconds.
    
    Returns:
        int: The current New York time in milliseconds.
    """
    # Get current UTC time
    utc_now = datetime.now(pytz.utc)
    # Convert UTC time to New York time
    beijing_tz = pytz.timezone('America/New_York')
    beijing_now = utc_now.astimezone(beijing_tz)
    # Convert New York time to milliseconds timestamp
    milliseconds = int(beijing_now.timestamp() * 1000)
    return milliseconds

def calculate_date_difference(date_str, timezone_str):
    """
    Calculates the difference in days between the current date and the specified date using the given timezone.
    
    Parameters:
        date_str (str): The date string to compare.
        timezone_str (str): The timezone string (e.g., 'America/New_York').
        
    Returns:
        int: The difference in days between the current date and the specified date.
    """
    # Convert the string date to a datetime object with the specified timezone
    date = pd.to_datetime(date_str).tz_localize(timezone_str)
    
    # Get current date and time in the given timezone
    current_date = datetime.now(pytz.timezone(timezone_str))
    
    # Calculate the difference between the current date and the given date
    date_diff = current_date - date
    
    # Return the difference in days
    return date_diff.days

def getUSStockHistoryByDate(symbol, start_date='2025-01-01', end_date='9999-12-31'):
    """
    Fetches historical stock data for a US symbol within the specified date range, including moving averages.
    
    Parameters:
        symbol (str): The US stock symbol.
        start_date (str, optional): The start date in 'YYYY-MM-DD' format. Defaults to '2025-01-01'.
        end_date (str, optional): The end date in 'YYYY-MM-DD' format. Defaults to '9999-12-31'.
        
    Returns:
        DataFrame: A pandas DataFrame containing historical data with 60-day and 120-day moving averages, formatted timestamps, and other processed columns.
    """
    timezone = 'America/New_York'
    begin = get_current_newyork_time()

    days = calculate_date_difference(start_date, timezone) + 120
    
    url = f'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={symbol}&begin={begin}&period=day&type=before&count=-{days}'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    
    # Extract column names and data items
    columns = response_json['data']['column']
    items = response_json['data']['item']

    # Convert data items to DataFrame and set column names
    df = pd.DataFrame(items, columns=columns)

    # Calculate 60-day moving average (MA60)
    df['MA60'] = df['close'].rolling(window=60).mean()
    # Calculate 120-day moving average (MA120)
    df['MA120'] = df['close'].rolling(window=120).mean()
    
    # Convert timestamp to pandas datetime object and filter
    df['Timestamp_str'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert(timezone)
    df = df[df['Timestamp_str'] >= start_date]
    df = df[df['Timestamp_str'] <= end_date]

    # Convert filtered timestamps to string format
    df['Timestamp_str'] = df['Timestamp_str'].dt.strftime('%Y-%m-%d')
    
    df['percent'] = df['percent'].div(100)
    df['turnoverrate'] = df['turnoverrate'].div(100)
    # Add Ticker column
    df['Ticker'] = symbol

    return df


if __name__ == "__main__":
    pass
    #df = getMinuteData('GOOG')
    # df.to_csv("GOOG.csv", index = 0)
    # df = getMinuteData('GOOGL')
    # df.to_csv("GOOGL.csv", index = 0)
    #ticker_list = ['SH019742']
    # ticker_list = ['SZ161125','SZ161130','SH513000','SH513300']
    # df = getETFQuote(ticker_list)
    #df.to_excel("etf.xlsx")
    # bond_ticker_list = ['SH019746','SH019742']
    # df = getBondQuote(bond_ticker_list)
    # df.to_excel("bond.xlsx")

    #stock_ticker_list = ['AAPL','GOOG']
    #df = getBatchQuote(stock_ticker_list)
    
    #df = getUSStockHistoryByDate(symbol = 'GOOGL', start_date = '2025-02-03')
    # symbols = ['SPY','QQQ']
    # df = getUSETFQuote(symbols)
    # df = getMinuteData('SZ161128')
