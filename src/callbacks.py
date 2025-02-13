import pandas as pd
import plotly.express as px  # 新增导入 Plotly Express
from dash import Input, Output, dcc

from qqqm_data import getQQQMHolding

df = getQQQMHolding()

def register_callbacks(app):
    """注册 Dash 回调函数"""

    def highlight_change(val):
        try:
            val = float(val)
            if val < 0:
                opacity = min(abs(val) / 0.1, 1)
                color = f'rgba(255, 0, 0, {opacity})'  # 红色渐变
            else:
                opacity = min(val / 0.1, 1)
                color = f'rgba(0, 255, 0, {opacity})'  # 绿色渐变
            return color
        except:
            return ''

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
        Output("stock-table", "style_data_conditional"),
        Input("stock-table", "data")
    )
    def update_intraday_return_styles(data):
        """应用 highlight_change 至 IntradayReturn 列"""
        styles = []
        if data:
            for i, row in enumerate(data):
                val = row.get("IntradayReturn")
                if val is None:
                    continue
                color = highlight_change(val)
                styles.append({
                    "if": { "row_index": i, "column_id": "IntradayReturn" },
                    "backgroundColor": color
                })
        return styles

    @app.callback(
        Output("download-csv", "data"),
        Input("download-csv-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def download_csv(n_clicks):
        """将 df 导出为 CSV 文件下载"""
        return dcc.send_data_frame(df.to_csv, "NASDAQ_100.csv", index=False)
