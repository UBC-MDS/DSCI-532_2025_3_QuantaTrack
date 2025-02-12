import pandas as pd
from dash import Input, Output

# 预设数据（模拟 NASDAQ 100 数据）
data = {
    "Ticker": ["AAPL", "NVDA", "MSFT", "AMZN", "AVGO", "META"],
    "Name": ["Apple Inc", "NVIDIA Corp", "Microsoft Corp", "Amazon.com Inc", "Broadcom Inc", "Meta Platforms Inc"],
    "Weight": ["8.68%", "8.03%", "7.70%", "6.09%", "4.39%", "3.94%"],
    "Price": [236.23, 130.97, 409.05, 230.67, 236.01, 725.01],
    "IntradayReturn": [1.55, -1.38, -0.58, -0.90, 0.41, 0.72],
    "Volume": ["28.06M", "123.99M", "10.64M", "19.29M", "10.40M", "8.69M"],
    "Amount": ["6.57B", "16.26B", "4.35B", "4.44B", "2.43B", "6.26B"],
    "MarketCap": ["3548.66B", "3207.33B", "3040.83B", "2444.58B", "1106.26B", "1836.93B"],
    "YTDReturn": [-5.56, -2.48, -2.95, 5.14, 1.80, 23.83],
    "Sector": ["Tech", "Tech", "Tech", "Consumer", "Tech", "Consumer"],
}

df = pd.DataFrame(data)

def register_callbacks(app):
    """注册 Dash 回调函数"""

    @app.callback(
        Output("stock-table", "data"),
        [Input("filter-ticker", "value"),
         Input("filter-name", "value"),
         Input("filter-sector", "value")]
    )
    def update_table(ticker, name, sector):
        """更新表格数据"""
        filtered_df = df.copy()

        # 按 Ticker 过滤（模糊匹配）
        if ticker:
            filtered_df = filtered_df[filtered_df["Ticker"].str.contains(ticker, case=False, na=False)]

        # 按 Name 过滤（模糊匹配）
        if name:
            filtered_df = filtered_df[filtered_df["Name"].str.contains(name, case=False, na=False)]

        # 按 Sector 过滤
        if sector and sector != "All":
            filtered_df = filtered_df[filtered_df["Sector"] == sector]

        return filtered_df.to_dict("records")

    @app.callback(
        Output("show-charts", "style"),
        [Input("show-charts", "value")]
    )
    def toggle_chart_visibility(show):
        """控制图表显示隐藏"""
        return {"display": "block" if show else "none"}
