import pandas as pd
import plotly.express as px  # 新增导入 Plotly Express
from dash import Input, Output, dcc
import dash

from qqqm_data import getQQQMHolding

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

    # 回调：每 n 秒更新数据，存入 dcc.Store（需在布局中添加 dcc.Store(id="data-store")）
    @app.callback(
        Output("data-store", "data"),
        Input("data-update-interval", "n_intervals")
    )
    def update_data(n_intervals):
        return getQQQMHolding().to_dict("records")

    # 回调：根据下拉菜单选择更新频率，修改 Interval 组件属性（需在布局中添加 dcc.Interval(id="data-update-interval")和 dcc.Dropdown(id="update-speed")）
    @app.callback(
        [Output("data-update-interval", "disabled"), Output("data-update-interval", "interval")],
        Input("update-speed", "value")
    )
    def update_interval_speed(value):
        if value == "3秒":
            return False, 3000
        elif value == "10秒":
            return False, 10000
        else:  # "不更新"
            return True, 1000  # interval 值无关紧要

    @app.callback(
        Output("stock-table", "data"),
        [Input("filter-ticker", "value"),
         Input("filter-name", "value"),
         Input("filter-sector", "value"),
         Input("data-store", "data")]
    )
    def update_table(ticker, name, sector, data):
        """更新表格数据"""
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if ticker:
            df = df[df["Ticker"].str.contains(ticker, case=False, na=False)]
        if name:
            df = df[df["Name"].str.contains(name, case=False, na=False)]
        if sector and sector != "All":
            df = df[df["Sector"] == sector]
        return df.to_dict("records")

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
        [Input("download-csv-btn", "n_clicks"),
         Input("data-store", "data")],
        prevent_initial_call=True
    )
    def download_csv(n_clicks, data):
        """当点击按钮时将数据导出为 CSV 文件下载"""
        ctx = dash.callback_context
        if not ctx.triggered or ctx.triggered[0]["prop_id"] != "download-csv-btn.n_clicks":
            # 如果不是按钮触发，则不进行下载
            from dash.exceptions import PreventUpdate
            raise PreventUpdate
        df = pd.DataFrame(data) if data else pd.DataFrame()
        def generate_csv_text(_):
            return df.to_csv(index=False)
        return dcc.send_string(generate_csv_text, "NASDAQ_100.csv")
