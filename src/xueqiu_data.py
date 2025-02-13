# %%
import requests
import pandas as pd
from datetime import datetime
import pytz

import requests

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
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

cookies = {
    "cookiesu": "501716971730603",
    "device_id": "b466cc5fe5c41c2cf5113e1dc9758e94",
    "s": "br1biz2pdb",
    "bid": "3f1caaa1da9c9048cf5319e6a0c33666_lwsmxccn",
    "remember": "1",
    "xq_a_token": "ad0c76ebec59c335683e9c829d229902421be184",
    "xqat": "ad0c76ebec59c335683e9c829d229902421be184",
    "xq_id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxMTA3NTAwNjIsImlzcyI6InVjIiwiZXhwIjoxNzQxMzI1NTA5LCJjdG0iOjE3Mzg3MzM3NzkyMjYsImNpZCI6ImQ5ZDBuNEFadXAifQ.o3ERaxqVjeTNJblmuRKENhbxML8EMGa0zQuiI4JMy38qDqK3QRcyYBOG2hnfJf1QGCS_1jtUacxjgLjEDwZ_cAeUCdHZ4a4PmFHIxLzwCm_cLg38T2d5NqddtaiceZFl-rmm4kzF6WAUEoAUrJXnrYn9yd4PWjA6pG1tr99und9iB-SZ78Tml0UGHyrka8Qt1ebJ6EVqDrlNABThY9utY9-a4pPnHknN-ooJ15O0rLhTIrqnhO8ZHSer-5ii6rpZuVCfu2xZFXt0YalPXQEcdKVJm5RpADv2ydqPZUDEI8X2GB1dyt2yOn6o8zwbPnV86nQIUQbCKo__gonzvHttnw",
    "xq_r_token": "fa088756ba361870080110924808b5fa01c3ef13",
    "xq_is_login": "1",
    "u": "2110750062",
    "Hm_lvt_1db88642e346389874251b5a1eded6e3": "1738819328,1738860881,1738891671,1739173290",
    "HMACCOUNT": "90AC0DA1311E6AC3",
    "Hm_lpvt_1db88642e346389874251b5a1eded6e3": "1739173300",
}



def getMinuteData(ticker):
    url = 'https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol='+ ticker +'&period=1d'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()

    # 提取所有字段并转换为DataFrame
    data_items = response_json['data']['items']

    # 移除不需要的字段
    for item in data_items:
        item.pop('macd', None)
        item.pop('kdj', None)
        item.pop('ratio', None)
        item.pop('capital', None)
        item.pop('volume_compare', None)

    df = pd.DataFrame(data_items)

    # 填充缺失值
    df.fillna({'high': df['current'], 'low': df['current']}, inplace=True)
    df['amount_total'] = df['amount_total'].ffill()
    df['volume_total'] = df['volume_total'].ffill()

    # 将 timestamp 转换为 pandas 的 datetime 对象
    df['Timestamp_str'] = pd.to_datetime(df['timestamp'].to_list(), unit='ms').tz_localize('UTC').tz_convert('America/New_York')
    df['Timestamp_str'] = df['Timestamp_str'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # 加入 Ticker 列
    df['Ticker'] = ticker

    return df

def getJson(symbols):
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail&is_delay_hk=false'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]

    return quote_data_list


def getBatchQuote(symbols):
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]

    # 将所有 quote 数据转换为 DataFrame，每个 quote 数据占一行
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
    # 将 timestamp 转换为 pandas 的 datetime 对象
    df['Timestamp_str'] = (
        pd.to_datetime(df['timestamp'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('America/New_York')
        .strftime('%Y-%m-%d %H:%M:%S %z')
    )

    # 填充缺失值
    df.fillna({'dividend': 0, 'dividend_yield': 0}, inplace=True)

    df['percent'] = df['percent'].div(100)
    df['current_year_percent'] = df['current_year_percent'].div(100)
    try:
        df['dividend_yield'] = df['dividend_yield'].div(100)
    except:
        pass
    

    return df

def getBondQuote(symbols):
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail'


    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]

    # 将所有 quote 数据转换为 DataFrame，每个 quote 数据占一行
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
    # 将 timestamp 转换为 pandas 的 datetime 对象
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

    # 将 timestamp 转换为 pandas 的 datetime 对象
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
    #symbols = ["IBTF","IBTG"]
    symbols_str = ','.join(symbols)
    url = 'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=' + symbols_str + '&extend=detail'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    quote_data_list = [item['quote'] for item in response_json['data']['items']]
    df = pd.DataFrame(quote_data_list)

    # 将 timestamp 转换为 pandas 的 datetime 对象
    df['Timestamp_str'] = (
        pd.to_datetime(df['timestamp'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('Asia/Shanghai')
        .strftime('%Y-%m-%d %H:%M:%S %z')
    )

    # 填充缺失值
    #df.fillna({'dividend': 0, 'dividend_yield': 0}, inplace=True)

    df['percent'] = df['percent'].div(100)
    df['current_year_percent'] = df['current_year_percent'].div(100)
    return df

def get_current_beijing_time():
    # 获取当前UTC时间
    utc_now = datetime.now(pytz.utc)
    # 将UTC时间转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_now = utc_now.astimezone(beijing_tz)
    # 将北京时间转换为毫秒时间戳
    milliseconds = int(beijing_now.timestamp() * 1000)
    return milliseconds

def getStockHistory(symbol,days = 30, begin = get_current_beijing_time()):
    """
    获取一个股票的日线历史数据。

    参数:
    symbol (str): 股票代码。
    days (int): 前推日数，默认为30天。
    begin (int): 开始前推的时间，默认为当前北京时间的毫秒时间戳。

    返回:
    pd.DataFrame: 包含股票日线历史数据的DataFrame。

    数据列:
    - timestamp: 时间戳（毫秒）
    - volume: 成交量
    - open: 开盘价
    - high: 最高价
    - low: 最低价
    - close: 收盘价
    - chg: 涨跌额
    - percent: 涨跌幅
    - turnoverrate: 换手率
    - amount: 成交额
    - volume_post: 盘后成交量
    - amount_post: 盘后成交额
    - Timestamp_str: 格式化的北京时间字符串
    - Ticker: 股票代码
    """

    url = f'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={symbol}&begin={begin}&period=day&type=before&count=-{days}'

    response = requests.get(url, headers=headers, cookies=cookies)
    response_json = response.json()
    
    # 提取列名和数据项
    columns = response_json['data']['column']
    items = response_json['data']['item']

    # 将数据项转换为 DataFrame，并设置列名
    df = pd.DataFrame(items, columns=columns)

    # 将 timestamp 转换为 pandas 的 datetime 对象
    df['Timestamp_str'] = (
        pd.to_datetime(df['timestamp'].to_list(), unit='ms')
        .tz_localize('UTC')
        .tz_convert('Asia/Shanghai')
        .strftime('%Y-%m-%d %H:%M:%S %z')
    )

    df['percent'] = df['percent'].div(100)
    # 加入 Ticker 列
    df['Ticker'] = symbol
    """
    df.columns = ['timestamp', 'volume', 'open', 'high', 'low', 'close', 'chg', 'percent',
       'turnoverrate', 'amount', 'volume_post', 'amount_post',
       'Timestamp_str','Ticker']
    """
    return df




# %%
if __name__ == "__main__":
    pass
    df = getMinuteData('AAPL')
    #ticker_list = ['SH019742']
    # ticker_list = ['SZ161125','SZ161130','SH513000','SH513300']
    # df = getETFQuote(ticker_list)
    #df.to_excel("etf.xlsx")
    # bond_ticker_list = ['SH019746','SH019742']
    # df = getBondQuote(bond_ticker_list)
    # df.to_excel("bond.xlsx")

    #stock_ticker_list = ['AAPL','GOOG']
    #df = getBatchQuote(stock_ticker_list)



# %%


# %%
