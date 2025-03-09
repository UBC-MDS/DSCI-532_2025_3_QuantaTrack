import pandas as pd
from dash import html, dcc, Input, Output
import dash

from src.layout import *
from src.components import *
from src.qqqm_data import getQQQMHolding

def highlight_change(val):
        try:
            val = float(val)
            if val < 0:
                opacity = min(abs(val) / 0.1, 1)
                color = f'rgba(255, 0, 0, {opacity})'  # Red gradient
            else:
                opacity = min(val / 0.1, 1)
                color = f'rgba(0, 255, 0, {opacity})'  # Green gradient
            return color
        except:
            return ''

def register_callbacks(app):
    """Register Dash callback functions""" 
        
    # Callback for updating pie chart based on sector selection
    @app.callback(
        Output("pie-chart-container", "children"),  # Output container for the pie chart
        Input("filter-sector", "value")  # Input: sector dropdown value
    )
    def update_pie_chart(selected_sectors):
        """Updates the pie chart based on selected sectors"""
        return html.Iframe(
            srcDoc=render_pie_chart(selected_sectors),  # Generate pie chart with selected sectors
            style={"border": "0", "width": "100%", "height": "350px"}  # Styling
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
            style={"border": "0", "width": "100%", "height": "350px"}
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
            style={"border": "0", "width": "100%", "height": "350px"}  # Style the iframe
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
            style={"border": "0", "width": "100%", "height": "350px"}
        )

    

    @app.callback(
    Output('stock-dropdown', 'options'),     # 输出到 stock-dropdown 的 options
    Output('stock-dropdown', 'value'),       # 也可以顺便更新一下默认选中的 value
    Input('filter-sector', 'value')          # 以 filter-sector 的 value 作为输入
    )
    def update_stock_dropdown(selected_sector):
        
        nasdaq100_tickers = getQQQMHolding()
        # 如果没有选或者选了 'All'，那就把全部股票都显示出来
        if not selected_sector or 'All' in selected_sector:
            filtered_df = nasdaq100_tickers
        else:
            # 如果 sector 是单选：用 == 过滤
            # 如果 sector 是多选：用 isin 过滤
            # 假设多选，这里写成 isin
            filtered_df = nasdaq100_tickers[nasdaq100_tickers['Sector'].isin(selected_sector)]
    
        # 生成新的 options
        new_options = [
            {'label': row['Name'], 'value': row['Ticker']}
            for _, row in filtered_df.iterrows()
        ]
        
        # 设定一个新的默认选项（比如取过滤后第一行）也可以不设置，设成 None
        new_value = None
        if len(filtered_df) > 0:
            new_value = filtered_df.iloc[0]['Ticker']
        
        return new_options, new_value


    
    # Callback for updating regression graph based on stock and time range selection
    @app.callback(
        Output('regression-graph-container', 'children'),
        [Input('stock-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_regression_graph(selected_stock, start_date, end_date):
        """Updates the regession and beta value based on selected stock and date range"""
        # 调用 render_regression_graph 函数，生成图表
        regression_fig_html = render_regression_graph(selected_stock, start_date, end_date)
    
        # 将生成的图表 HTML 结果嵌入 Iframe 中
        return html.Iframe(
            srcDoc=regression_fig_html, style={"border": "0", "width": "100%", "height": "600px"}
        )

    # Callback for updating trend graph based on stock and time range selection
    @app.callback(
        Output('price-trend-graph-container', 'children'),
        [Input('stock-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_trend_graph(selected_stock, start_date, end_date):
        """Updates the trend graph based on selected stock and date range"""
        # 调用 render_trend_graph 函数，生成图表
        price_trend_fig_html = render_trend_graph(selected_stock, start_date, end_date)
    
        # 将生成的图表 HTML 结果嵌入 Iframe 中
        return html.Iframe(
            srcDoc=price_trend_fig_html, style={"border": "0", "width": "100%", "height": "600px"}
        )
    

    

    # Callback: Update data every n seconds and store it in dcc.Store (requires adding dcc.Store(id="data-store") in the layout)
    @app.callback(
        Output("data-store", "data"),
        Input("data-update-interval", "n_intervals")
    )
    def update_data(n_intervals):
        return getQQQMHolding().to_dict("records")

    # Callback: Update the interval frequency based on the dropdown selection, modifying the Interval component's properties 
    # (requires adding dcc.Interval(id="data-update-interval") and dcc.Dropdown(id="update-speed") in the layout)
    @app.callback(
        [Output("data-update-interval", "disabled"), Output("data-update-interval", "interval")],
        Input("update-speed", "value")
    )
    def update_interval_speed(value):
        if value == "3s":
            return False, 3000
        elif value == "10s":
            return False, 10000
        else:  # "No update"
            return True, 1000  # interval value doesn't matter


    @app.callback(
        Output("stock-table", "rowData"),
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
        
        return dcc.send_string(df.to_csv(index=False), "QuantaTrack_Output.csv")
        # def generate_csv_text(_):
        #     return df.to_csv(index=False)
        # return dcc.send_string(generate_csv_text, "QuantaTrack_Output.csv")
