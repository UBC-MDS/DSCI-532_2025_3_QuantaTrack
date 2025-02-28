import pandas as pd
import numpy as np
import re
import plotly.express as px  # 新增导入 Plotly Express
from dash import html, dcc, Input, Output
import dash

from layout import *
from qqqm_data import getQQQMHolding
from xueqiu_data import getUSStockHistoryByDate


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
        
    # Callback for updating pie chart based on sector selection
    @app.callback(
        Output("pie-chart-container", "children"),  # Output container for the pie chart
        Input("filter-sector", "value")  # Input: sector dropdown value
    )
    def update_pie_chart(selected_sectors):
        """Updates the pie chart based on selected sectors"""
        return html.Iframe(
            srcDoc=render_pie_chart(selected_sectors),  # Generate pie chart with selected sectors
            style={"border": "0", "width": "100%", "height": "600px"}  # Styling
        )
        
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
        
    # New callback: Update YTD Distribution
    @app.callback(
        Output("ytd-dist-container", "children"),
        Input("filter-sector", "value")
    )
    def update_ytd_dist(selected_sectors):
        # If user clears the dropdown, default to ["All"]
        if not selected_sectors:
            selected_sectors = ["All"]

        return html.Iframe(
            srcDoc=render_ytd_distribution(selected_sectors),
            style={"border": "0", "width": "100%", "height": "600px"}
        )

    # New callback: Update Top/Bottom 5 Chart
    @app.callback(
        Output("intraday-contribution-top5-bottom5-container", "children"),
        Input("filter-sector", "value")
    )
    def update_intraday_bar(selected_sectors):
        if not selected_sectors:
            selected_sectors = ["All"]

        return html.Iframe(
            srcDoc=render_intraday_contribution_5(selected_sectors),
            style={"border": "0", "width": "100%", "height": "600px"}
        )

    # Callback for updating regression and trnde graph based on stock and time range selection
    @app.callback(
        [Output('regression-graph-container', 'children'),
         Output('price-trend-graph-container', 'children')],
        [Input('stock-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_regression_and_trend_graph(selected_stock, start_date, end_date):
        """Updates the regession and beta value as well as trend based on selected stock and date range"""
        # 调用图一的 render_regression_and_trend_graph 函数，生成图表
        regression_fig_html, price_trend_fig_html = render_regression_and_trend_graph(selected_stock, start_date, end_date)
    
        # 将生成的图表 HTML 结果嵌入 Iframe 中
        return html.Iframe(
            srcDoc=regression_fig_html, style={"border": "0", "width": "100%", "height": "600px"}
        ), html.Iframe(
            srcDoc=price_trend_fig_html, style={"border": "0", "width": "100%", "height": "600px"}
        )



    
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
         Input("data-store", "data"),
         Input("filter-sector", "value")],
        prevent_initial_call=True
    )
    def download_csv(n_clicks, data, sectors):
        """当点击按钮时将数据导出为 CSV 文件下载"""
        ctx = dash.callback_context
        if not ctx.triggered or ctx.triggered[0]["prop_id"] != "download-csv-btn.n_clicks":
            # 如果不是按钮触发，则不进行下载
            from dash.exceptions import PreventUpdate
            raise PreventUpdate
        
        df = pd.DataFrame(data) if data else pd.DataFrame()

        # Filter by sectors (handling multiple selections)
        if sectors and "All" not in sectors:
            df = df[df["Sector"].isin(sectors)]  # Filter to keep rows with sectors in the selected list
        
        return dcc.send_string(df.to_csv(index=False), "NASDAQ_100.csv")
        # def generate_csv_text(_):
        #     return df.to_csv(index=False)
        # return dcc.send_string(generate_csv_text, "QuantaTrack_Output.csv")
