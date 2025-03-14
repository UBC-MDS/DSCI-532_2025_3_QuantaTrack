import pickle
import os
import datetime
import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px
from pyecharts import options as opts
from src.qqqm_data import getQQQMHolding
from src.xueqiu_data import getUSStockHistoryByDate
from src.components import calculate_beta, fetch_stock_data, render_regression_graph, render_trend_graph


TICKER = ['AAPL']
CACHE_FILE = "nasdaq100_cache.pkl"
START_DATE = "2024-01-01"
END_DATE   = "2025-01-01"

def precompute_nasdaq100():
    
    # 如果已存在缓存文件，先读出来，避免重复计算
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache_data = pickle.load(f)
    else:
        cache_data = {}

    for symbol in TICKER:
        # 为回归图、趋势图各定义一个 key
        key_regression = f"regression|{symbol}"
        key_trend = f"trend|{symbol}"

        # 若缓存里没有，就调用函数生成并存储
        if key_regression not in cache_data:
            fig_reg = render_regression_graph(symbol, START_DATE, END_DATE)
            cache_data[key_regression] = fig_reg

        if key_trend not in cache_data:
            fig_trend = render_trend_graph(symbol, START_DATE, END_DATE)
            cache_data[key_trend] = fig_trend

    # 把更新后的字典写回到文件
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache_data, f)

    print(f"Precomputation finished and cached {len(cache_data)} graphs into {CACHE_FILE}。")

if __name__ == "__main__":
    precompute_nasdaq100()
