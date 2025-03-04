import pandas as pd
from dash import html, dcc, Input, Output, State
import dash

from src.layout import *
from src.plotting import *
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
            style={"border": "0", "width": "100%", "height": "600px"}  # Styling
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


    # Callback function: Update the sorting status and arrow display based on header clicks in a loop
    @app.callback(
        Output("stock-table", "data", allow_duplicate=True),
        Output("stock-table", "columns", allow_duplicate=True),
        Output("sort-state", "data", allow_duplicate=True),
        Output("original-data", "data", allow_duplicate=True),
        Output("stock-table", "sort_by", allow_duplicate=True),
        Input("stock-table", "sort_by"),
        State("sort-state", "data"),
        State("stock-table", "data"),
        State("original-data", "data"),
        prevent_initial_call=True
    )
    def update_sort(sort_by, sort_state, data, original_data):
        # Initialize original data
        if not original_data:
            original_data = data
        
        # Determine the column to be sorted
        if sort_by:
            sort_col = sort_by[0]["column_id"]
        else:
            # Use existing click record if no new sort_by
            sort_col = sort_state.get("last_sorted")
            if not sort_col:
                return data, original_columns, sort_state, original_data, sort_by

        # Calculate the new sort direction based on the previous state
        prev = sort_state.get(sort_col, "none")
        if prev == "none":
            new_direction = "asc"
        elif prev == "asc":
            new_direction = "desc"
        else:
            new_direction = "none"
        # Reset sort state and record the current clicked column
        sort_state = {col_def["id"]: "none" for col_def in original_columns}
        sort_state["last_sorted"] = sort_col
        sort_state[sort_col] = new_direction

        # Update column headers and add arrow indicators
        new_columns = []
        for col_def in original_columns:
            cid = col_def["id"]
            base_name = col_def["name"].split(" ")[0]
            arrow = ""
            if sort_state.get(cid, "asc") == "asc":
                arrow = " ↑"
            elif sort_state.get(cid, "desc") == "desc":
                arrow = " ↓"
            new_columns.append({**col_def, "name": base_name + arrow})

        # Update data: if direction is "none", restore original, otherwise sort the data
        if new_direction == "none":
            sorted_data = original_data
            sort_by = []  # Clear sort state
        else:
            reverse = True if new_direction == "desc" else False
            sorted_data = sorted(data, key=lambda row: row.get(sort_col, None), reverse=reverse)

        return sorted_data, new_columns, sort_state, original_data, sort_by
