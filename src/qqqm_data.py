# %%
import requests
import pandas as pd
from io import BytesIO

from src.xueqiu_data import getBatchQuote
# 添加缓存变量
_ndx_holding_cache = None

def downloadQQQMHolding():
    global _ndx_holding_cache
    if _ndx_holding_cache is not None:
        return _ndx_holding_cache

    try:
        # Send a GET request to the URL
        url = "https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=QQQM"  
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # 使用 BytesIO 将字节内容转换为文件对象
        content_io = BytesIO(response.content)
        # 使用 pandas 读取 CSV 内容
        df = pd.read_csv(content_io)
        _ndx_holding_cache = df  # 缓存数据
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the CSV file: {e}")

# 清理df
def getQQQMHolding():
    df = downloadQQQMHolding()
    df = df.rename(columns={'Holding Ticker': 'Ticker'})
    df['Ticker'] = df['Ticker'].str.strip()

    valid_classes = ['Common Stock', 'American Depository Receipt', 'American Depository Receipt - NY']
    df = df[df['Class of Shares'].isin(valid_classes)]

    filter_column = ['Ticker', 'Name', 'Weight', 'Sector', 'Class of Shares']
    df = df[filter_column]

    # 将 Weight 列转换为数值类型
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
    df["Weight"] = df["Weight"] / df["Weight"].sum()

    xueqiu_df= getBatchQuote(df['Ticker'])

    # 在 Ticker 列上进行合并
    merged_df = pd.merge(df,xueqiu_df,left_on='Ticker',right_on = 'symbol')
    
    # 排序

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
        'profit_four':'Profit_TTM',
        'Timestamp_str':'Date',
    })
    merged_df['IntradayContribution'] = merged_df['Weight'] * merged_df['IntradayReturn']
    merged_df['YTDContribution'] = merged_df['Weight'] * merged_df['YTDReturn']

    output_columns = ['Ticker', 'Name', 'Weight', 'Price','IntradayReturn',
                      'Volume','Amount','IntradayContribution',
                        'MarketCap', 'YTDReturn','YTDContribution',
                        'PE','PB','Profit_TTM', 'DividendYield','Dividend',
                        'SharesOutstanding','Sector','Date']
    merged_df = merged_df[output_columns]

    return merged_df


    
if __name__ == "__main__":
    df = getQQQMHolding()
    print(df)



# %%
