import pandas as pd
import re
import plotly.express as px  # 新增导入 Plotly Express
from dash import html, dcc, Input, Output
import dash

from layout import *
from qqqm_data import getQQQMHolding

def register_callbacks(app):
    """注册 Dash 回调函数"""
    
    # Callback for scatter plot based on sector filter
    @app.callback(
        Output("scatter-plot-container", "children"),  # Output container for scatter plot
        Input("filter-sector", "value")  # Input: sector dropdown value
    )
    def update_scatter_plot(selected_sectors):
        # Call render_scatter_plot function with the selected sectors and return the HTML
        return html.Iframe(
            srcDoc=render_scatter_plot(selected_sectors),  # Generate the chart with selected sectors
            style={"border": "0", "width": "100%", "height": "600px"}  # Style the iframe
        )

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
        if value == "3s":
            return False, 3000
        elif value == "10s":
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
    def update_table(ticker, name, sectors, data):
        """更新表格数据"""
        df = pd.DataFrame(data) if data else pd.DataFrame()

        # # Apply sector filter (if "All" is selected, no filtering is applied)
        # if "All" not in selected_sectors:  # Only filter if "All" is not selected
        #     df = df[df["Sector"].isin(selected_sectors)]  # Use isin to support multi-sector selection  
        if ticker:
            df = df[df["Ticker"].str.contains(ticker, case=False, na=False)]
        if name:
            df = df[df["Name"].str.contains(name, case=False, na=False)]

        # Filter by sectors (handling multiple selections)
        if sectors and "All" not in sectors:
            df = df[df["Sector"].isin(sectors)]  # Filter to keep rows with sectors in the selected list
        
        return df.to_dict("records")
        
        # # Apply ticker filter (if provided)
        # if ticker:
        #     if isinstance(ticker, list):  # If ticker is a list, use vectorized str.contains with OR condition
        #         ticker_pattern = "|".join([re.escape(t) for t in ticker])  # Create regex pattern
        #         df = df[df["Ticker"].str.contains(ticker_pattern, case=False, na=False)]
        #     else:  # Single ticker value
        #         df = df[df["Ticker"].str.contains(ticker, case=False, na=False)]

        # # Apply name filter (if provided)
        # if name:
        #     if isinstance(name, list):  # If name is a list, use vectorized str.contains with OR condition
        #         name_pattern = "|".join([re.escape(n) for n in name])  # Create regex pattern
        #         df = df[df["Name"].str.contains(name_pattern, case=False, na=False)]
        #     else:  # Single name value
        #         df = df[df["Name"].str.contains(name, case=False, na=False)]

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
         # Input("filter-sector", "value")],
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
        print(df)

        # Apply sector filter (if "All" is selected, no filtering is applied)
        # if "All" not in selected_sectors:  # Only filter if "All" is not selected
        #     df = df[df["Sector"].isin(selected_sectors)]  # Use isin to support multi-sector selection
        
        return dcc.send_string(df.to_csv(index=False), "NASDAQ_100.csv")
        # def generate_csv_text(_):
        #     return df.to_csv(index=False)
        # return dcc.send_string(generate_csv_text, "NASDAQ_100.csv")
