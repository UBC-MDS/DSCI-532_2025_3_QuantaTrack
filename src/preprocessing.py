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
    """
    Precomputes and caches regression and trend graphs for a predefined set of 
    NASDAQ 100 tickers within a specified date range.

    This function:
        1. Checks if a cache file (defined by CACHE_FILE) already exists.
           - If it exists, loads previously cached graph data from this file.
           - Otherwise, initializes an empty cache dictionary.
        2. Iterates through a list of tickers (defined by TICKER).
           - For each ticker, constructs cache keys for the regression graph 
             and the trend graph.
           - If the corresponding key is not found in the cache, the function 
             generates the graph using `render_regression_graph` or 
             `render_trend_graph`, then stores the result in the cache.
        3. Saves (pickles) the updated cache dictionary back to the cache file.
        4. Prints a summary indicating how many graphs have been cached.

    Global Variables (assumed to be defined elsewhere):
        - TICKER (list): A list of NASDAQ 100 ticker symbols.
        - START_DATE (str): The start date for the historical data (e.g., 'YYYY-MM-DD').
        - END_DATE (str): The end date for the historical data (e.g., 'YYYY-MM-DD').
        - CACHE_FILE (str): The path to the pickle file used for caching.

    Side Effects:
        - Reads and writes a pickle file to store the cached graphs.
        - Prints a message summarizing the caching operation.

    Returns:
        None
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache_data = pickle.load(f)
    else:
        cache_data = {}

    for symbol in TICKER:
    
        key_regression = f"regression|{symbol}"
        key_trend = f"trend|{symbol}"

        if key_regression not in cache_data:
            fig_reg = render_regression_graph(symbol, START_DATE, END_DATE)
            cache_data[key_regression] = fig_reg

        if key_trend not in cache_data:
            fig_trend = render_trend_graph(symbol, START_DATE, END_DATE)
            cache_data[key_trend] = fig_trend

    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache_data, f)

    print(f"Precomputation finished and cached {len(cache_data)} graphs into {CACHE_FILE}。")

if __name__ == "__main__":
    precompute_nasdaq100()
