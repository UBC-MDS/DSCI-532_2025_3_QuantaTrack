import requests
import pandas as pd
from datetime import datetime
import pytz

import requests


# Extract headers
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133")',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# Extract cookies
cookies = {
    "cookiesu": "501716971730603",
    "device_id": "b466cc5fe5c41c2cf5113e1dc9758e94",
    "s": "br1biz2pdb",
    "bid": "3f1caaa1da9c9048cf5319e6a0c33666_lwsmxccn",
    "remember": "1",
    "xq_is_login": "1",
    "u": "2110750062",
    "Hm_lvt_1db88642e346389874251b5a1eded6e3": "1739854474,1739914865,1739951903,1739995087",
    "HMACCOUNT": "90AC0DA1311E6AC3",
    "xq_a_token": "c0624837776ef160538ea564c1226a031c57eda2",
    "xqat": "c0624837776ef160538ea564c1226a031c57eda2",
    "xq_id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxMTA3NTAwNjIsImlzcyI6InVjIiwiZXhwIjoxNzQyNjI0MDIxLCJjdG0iOjE3NDAwMzIwMjExNzUsImNpZCI6ImQ5ZDBuNEFadXAifQ.bjooTOEJnB7JmE9BELAWuBLaIG3itZgjq5tH8WmLJW1rsSvg2jhD2fDCjVgVxIdFRRmaEe1BW9abjBtv4EIqAEOtiCTJSBgCd3cqNaK6j6a0PLjrtj2v3YFwcqcsFuZnioNM53bZ6-YZOdOxhkU51Z_wGVXmfLSLo4Y84kciCN2eL6Ybt_9fKlUPMRftdNUh92qOpN9186jfJ9ThuhbM1HrAlizQEatN3geMJCQyQ_O6vhDMv5Z6iNF4X8xXte6t4KE1Yqj-DeBiJaZ3D_IsIWsWEVu7fR3GZEphgoVFFeUcvwTbzithBuCVGXkR-bNpMctvJPvJWzeZxbmQeLasmg",
    "xq_r_token": "0860346c7cb5f3e8be2929ecc09698c3f53608dc",
    "is_overseas": "1",
    "Hm_lpvt_1db88642e346389874251b5a1eded6e3": "1740036370",
}

def getMinuteData(ticker):
    """
    Fetches minute-level stock data for a given ticker from Xueqiu API, processes it into a DataFrame,
    and fills missing values. Adds the last close price and ticker to the DataFrame.
    """
    url = 'https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol='+ ticker +'&period=1d'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    last_close = response_json['data']['last_close']
    # Extract all fields and convert them into DataFrame
    data_items = response_json['data']['items']

    # Remove unnecessary fields
    for item in data_items:
        item.pop('macd', None)
        item.pop('kdj', None)
        item.pop('ratio', None)
        item.pop('capital', None)
        item.pop('volume_compare', None)

    df = pd.DataFrame(data_items)

    # Fill missing values
    df.fillna({'high': df['current'], 'low': df['current']}, inplace=True)
    df['amount_total'] = df['amount_total'].ffill()
    df['volume_total'] = df['volume_total'].ffill()

    # # 转换为 datetime 类型（毫秒级时间戳）
    # df['Timestamp_str'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)

    # # 确保转换后的 datetime 列是 DatetimeIndex
    # df['Timestamp_str'] = df['Timestamp_str'].dt.tz_convert('America/New_York')

    # # 以字符串格式存储
    # df['Timestamp_str'] = df['Timestamp_str'].dt.strftime('%Y-%m-%d %H:%M:%S %z')

    # Add Ticker column
    df['Ticker'] = ticker

    df['LastClose']=last_close

    return df

def getJson(symbols):
    """
    Fetches batch stock quote data for the given symbols from Xueqiu API and returns the quote data as a list.
    """
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail&is_delay_hk=false'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]

    return quote_data_list


def getBatchQuote(symbols):
    """
    Fetches batch stock quote data for the given symbols from Xueqiu API and processes it into a DataFrame.
    Converts timestamps, fills missing values, and scales percentage values.
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


def getBondQuote(symbols):
    """
    Fetches bond quote data for the given symbols from Xueqiu API and returns it as a DataFrame.
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
       'high52w', 'low52w', 'limit_up', 'limit_down', 'volume_ratio',
       'par_value', 'circulation', 'close_dirty_price', 'coupon_rate',
       'list_date', 'maturity_date', 'value_dates', 'termtomaturity',
       'accrued_interest', 'dis_next_pay_date', 'convert_rate', 'payment_mode',
       'variety_type', 'new_issue_rating', 'credit_rating', 'rating',
       'Timestamp_str']
    """
    # Convert timestamp to pandas datetime object
    df['Timestamp_str'] = (
        pd.to_datetime(df['timestamp'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('Asia/Shanghai')
        .strftime('%Y-%m-%d %H:%M:%S %z')
    )
    df['list_date_str'] = (
        pd.to_datetime(df['list_date'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('Asia/Shanghai')
        .strftime('%Y-%m-%d')
    )
    df['maturity_date_str'] = (
        pd.to_datetime(df['maturity_date'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('Asia/Shanghai')
        .strftime('%Y-%m-%d')
    )
    # 填充缺失值
    #df.fillna({'dividend': 0, 'dividend_yield': 0}, inplace=True)

    df['percent'] = df['percent'].div(100)
    df['current_year_percent'] = df['current_year_percent'].div(100)

    df['coupon_rate'] = df['coupon_rate'].div(100)
    return df

def getETFQuote(symbols):
    """
    Fetches ETF quote data for the given symbols from Xueqiu API and returns it as a DataFrame.
    """
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]
    df = pd.DataFrame(quote_data_list)
    '''
    output_colnames=['symbol', 'code', 'exchange', 'name', 'type', 'sub_type', 'status',
       'current', 'currency', 'percent', 'chg', 'timestamp', 'time',
       'lot_size', 'tick_size', 'open', 'last_close', 'high', 'low',
       'avg_price', 'volume', 'amount', 'turnover_rate', 'amplitude',
       'market_capital', 'float_market_capital', 'total_shares',
       'float_shares', 'issue_date', 'lock_set', 'current_year_percent',
       'high52w', 'low52w', 'limit_up', 'limit_down', 'volume_ratio',
       'unit_nav', 'acc_unit_nav', 'premium_rate', 'found_date',
       'expiration_date', 'nav_date', 'iopv']
    '''

    # Convert timestamp to pandas datetime object
    df['Timestamp_str'] = (
        pd.to_datetime(df['timestamp'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('Asia/Shanghai')
        .strftime('%Y-%m-%d %H:%M:%S %z')
    )
    df['NAV_Date_str'] = (
        pd.to_datetime(df['nav_date'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('Asia/Shanghai')
        .strftime('%Y-%m-%d')
    )
    # 填充缺失值
    #df.fillna({'dividend': 0, 'dividend_yield': 0}, inplace=True)

    df['percent'] = df['percent'].div(100)
    df['current_year_percent'] = df['current_year_percent'].div(100)

    df['premium_rate'] = df['premium_rate'].div(100)

    return df


def getUSETFQuote(symbols):
    """
    Fetches US ETF quote data for the given symbols from Xueqiu API and returns it as a DataFrame.
    """
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]
    df = pd.DataFrame(quote_data_list)

    # Convert timestamp to pandas datetime object
    df['Timestamp_str'] = (
        pd.to_datetime(df['timestamp'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('America/New_York')
        .strftime('%Y-%m-%d %H:%M:%S %z')
    )

    # 填充缺失值
    #df.fillna({'dividend': 0, 'dividend_yield': 0}, inplace=True)

    df['percent'] = df['percent'].div(100)
    df['current_year_percent'] = df['current_year_percent'].div(100)
    return df

def get_current_beijing_time():
    """
    Returns the current time in Beijing as a milliseconds timestamp.
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
    Returns the current time in New York as a milliseconds timestamp.
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
    Calculates the difference in days between the current date and the given date for a specified timezone.
    """
    # Convert the string date to a datetime object with the specified timezone
    date = pd.to_datetime(date_str).tz_localize(timezone_str)
    
    # Get current date and time in the given timezone
    current_date = datetime.now(pytz.timezone(timezone_str))
    
    # Calculate the difference between the current date and the given date
    date_diff = current_date - date
    
    # Return the difference in days
    return date_diff.days

def getUSStockHistoryByDate(symbol, start_date = '2025-01-01', end_date = '9999-12-31'):
    """
    Fetches historical stock data for a US symbol within the specified date range, including moving averages.
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

def getChinaStockHistoryByDate(symbol, start_date = '2025-01-01', end_date = '9999-12-31'):
    """Fetches historical stock data for a China symbol within the specified date range, including moving averages.
    """
    timezone = 'Asia/Shanghai'
    begin = get_current_beijing_time()

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

# def getStockHistory(symbol,days = 30, timezone = 'Asia/Shanghai'):
#     """
#     获取一个股票的日线历史数据。

#     参数:
#     symbol (str): 股票代码。
#     days (int): 前推日数，默认为30天。
#     begin (int): 开始前推的时间，默认为当前北京时间的毫秒时间戳。

#     返回:
#     pd.DataFrame: 包含股票日线历史数据的DataFrame。

#     数据列:
#     - timestamp: 时间戳（毫秒）
#     - volume: 成交量
#     - open: 开盘价
#     - high: 最高价
#     - low: 最低价
#     - close: 收盘价
#     - chg: 涨跌额
#     - percent: 涨跌幅
#     - turnoverrate: 换手率
#     - amount: 成交额
#     - volume_post: 盘后成交量
#     - amount_post: 盘后成交额
#     - Timestamp_str: 格式化的北京时间字符串
#     - Ticker: 股票代码
#     """
#     if timezone == 'Asia/Shanghai':
#         begin = get_current_beijing_time()
#     elif timezone == 'America/New_York':
#         begin  =get_current_newyork_time()

#     url = f'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={symbol}&begin={begin}&period=day&type=before&count=-{days}'

#     response = requests.get(url, headers=headers, cookies=cookies)
#     response_json = response.json()
    
#     # 提取列名和数据项
#     columns = response_json['data']['column']
#     items = response_json['data']['item']

#     # 将数据项转换为 DataFrame，并设置列名
#     df = pd.DataFrame(items, columns=columns)

#     # 将 timestamp 转换为 pandas 的 datetime 对象
#     df['Timestamp_str'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)\
#                            .dt.tz_convert(timezone)\
#                            .dt.strftime('%Y-%m-%d %H:%M:%S %z')

#     df['percent'] = df['percent'].div(100)
#     # 加入 Ticker 列
#     df['Ticker'] = symbol
#     """
#     df.columns = ['timestamp', 'volume', 'open', 'high', 'low', 'close', 'chg', 'percent',
#        'turnoverrate', 'amount', 'volume_post', 'amount_post',
#        'Timestamp_str','Ticker']
#     """
#     return df

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
