import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback, Input, Output, State
import pandas as pd

from pyecharts.charts import Pie
import plotly.graph_objects as go
import plotly.express as px
from pyecharts import options as opts
from qqqm_data import getQQQMHolding


def render_pie_chart(selected_sectors=["All"]):
    # 1. 获取并处理数据
    _df = getQQQMHolding()
    
    if "All" not in selected_sectors:
        _df = _df[_df["Sector"].isin(selected_sectors)]  # Apply sector filtering

    df_group = _df.groupby('Name', as_index=False).agg({'Weight': 'sum'})
    df_group = df_group.sort_values(by='Weight', ascending=False)
    top_10 = df_group.nlargest(10, 'Weight')
    rest = df_group.iloc[10:]
    rest_combined = pd.DataFrame({'Name': ['Other Companies'], 'Weight': [rest['Weight'].sum()]})
    combined_df = pd.concat([top_10, rest_combined], ignore_index=True)
    
    # 2. 组装 (名称, 权重) 列表
    data = list(zip(combined_df['Name'], combined_df['Weight']))

    # 3. 为前 10 项指定不同颜色
    colors= [
        "#08306b", "#08519c", "#2171b5", "#4292c6", "#6baed6",
        "#9ecae1", "#c6dbef", "#deebf7", "#f7fbff", "#cccccc"]

    # 4. 创建环形图
    chart = (
        Pie()
        .add(
            series_name="",
            data_pair=data,
            radius=["40%", "75%"],  # 环形图的内外半径
            center=["50%", "50%"]   # 图表居中
        )
        .set_colors(colors)  # 为每个扇区设置颜色
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="NASDAQ 100 Companies by Weight", 
                pos_left="center"
            ),
            legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {d}%")
        )
    )

    # 5. 返回嵌入式 HTML
    return chart.render_embed()

# Function to render the scatter plot based on selected sectors
def render_scatter_plot(selected_sectors):
    # 1. 获取并处理数据
    _df = getQQQMHolding()

    # 2. 如果有筛选的 sectors, 根据它们过滤数据
    selected_sectors = selected_sectors or ["All"]
    if "All" not in selected_sectors:  # Only filter if "All" is not selected
        _df = _df[_df["Sector"].isin(selected_sectors)]  # Filter by selected sectors

    # 3. 清洗和准备数据
    scatter_data = []
    for index, row in _df.iterrows():
        if pd.notna(row['DividendYield']) and pd.notna(row['PE']):  # Only take rows with valid values
            scatter_data.append(
                {
                    "x": row['PE'],  # X-axis: PE (Forward PE or other PE)
                    "y": row['DividendYield'],  # Y-axis: Dividend Yield
                    "text": f"{row['Ticker']} - {row['Name']}<br>Sector = {row['Sector']}<br>Dividend Yield = {row['DividendYield']}%<br>PE = {row['PE']}",  # Tooltip with Sector
                    "name": row['Name'],  # Display company name in legend (if needed)
                    "sector": row['Sector']  # Store sector information for color coding
                }
            )

    # 4. 创建 Plotly 散点图
    fig = go.Figure()

    # Create a color map for sectors
    unique_sectors = _df['Sector'].unique()  # Get unique sectors
    sector_to_color = {sector: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] 
                       for i, sector in enumerate(unique_sectors)}  # Map sector to a color using a color palette

    # 5. 创建 Plotly 散点图
    fig = go.Figure()

    # Add data points to the figure, color by sector
    for data in scatter_data:
        fig.add_trace(go.Scatter(
            x=[data['x']],
            y=[data['y']],
            mode='markers',
            text=data['text'],  # Tooltip content
            name=data['name'],  # Company name in legend (if needed)
            marker=dict(
                size=10,  # Adjust marker size
                color=sector_to_color.get(data['sector'], 'rgba(0, 0, 0, 0.7)'),  # Color by sector (default to black if sector not in map)
            )
        ))

    # 5. Update layout
    fig.update_layout(
        title="Dividend Yield vs. PE",
        title_font=dict(size=24, color="black", family="Calibri", weight="bold"),
        title_x=0.5,
        xaxis_title="PE",
        yaxis_title="Dividend Yield",
        hovermode='closest',  # Show the closest points in hover
        showlegend=False,  # Remove the legend
        plot_bgcolor="rgba(255, 255, 255, 0)",  # Transparent background for the plot
        paper_bgcolor="white",  # White background for the entire figure
        xaxis=dict(
            range=[0, 100],  # Limit x-axis from 0 to 100
            showgrid=True,  # Show grid lines
            zeroline=True,  # Show zero line
            gridcolor='rgba(0, 0, 0, 0.1)',  # Light gray grid lines
            showline=True,  # Show outer axis line (border)
            linewidth=1,  # Reduced border thickness for the x-axis
            linecolor='black'  # Outer line color for the x-axis
        ),
        yaxis=dict(
            showgrid=True,  # Show grid lines
            zeroline=True,  # Show zero line
            gridcolor='rgba(0, 0, 0, 0.1)',  # Light gray grid lines
            showline=True,  # Show outer axis line (border)
            linewidth=1,  # Reduced border thickness for the y-axis
            linecolor='black',  # Outer line color for the y-axis
            tickformat=".0%",  # Format the ticks as percentages
        ),
        # Full border around the whole chart
        margin=dict(l=50, r=50, t=50, b=50),  # Add margins to ensure full border
        shapes=[
            dict(
                type="rect",  # Shape type is rectangle
                x0=0, x1=1, y0=0, y1=1,  # Full area of the plot
                xref="paper", yref="paper",  # Reference to paper coordinates (entire figure)
                line=dict(color="black", width=1)  # Black border with thinner thickness
            )
        ]
    )

    # 6. Return the figure's HTML
    return fig.to_html(full_html=False)

def render_ytd_distribution(selected_sectors=["All"]):
    """
    Renders a histogram with kernel density overlay 
    for YTD Return, including vertical lines for mean & median.
    """
    df = getQQQMHolding()

    # Apply sector filtering
    if "All" not in selected_sectors:
        df = df[df["Sector"].isin(selected_sectors)]

    # Ensure YTDReturn is numeric
    df["YTDReturn"] = pd.to_numeric(df["YTDReturn"], errors="coerce")

    # Drop NaNs
    df = df.dropna(subset=["YTDReturn"])

    # Basic histogram with Plotly Express
    fig = px.histogram(
        df, 
        x="YTDReturn", 
        nbins=20, 
        #title="YTD Return Distribution", 
        opacity=0.5
    )
    fig.update_traces(name="YTDReturn")

    # Add kernel density for smooth curve
    fig.add_trace(
        px.histogram(df, x="YTDReturn", nbins=20, histnorm="probability density").data[0]
    )
    fig.data[1].marker = dict(opacity=0)  # Hide second histogram bars, keep the curve
    #fig.data[1].line = dict(color="blue", width=2)

    # Calculate mean & median
    mean_val = df["YTDReturn"].mean()
    median_val = df["YTDReturn"].median()

    # Add lines for mean (green) & median (red)
    fig.add_vline(x=mean_val, line_width=2, line_dash="solid", line_color="green",
                  annotation_text=f"Mean: {mean_val:.2%}",
                  annotation_position="top right")
    fig.add_vline(x=median_val, line_width=2, line_dash="solid", line_color="red",
                  annotation_text=f"Median: {median_val:.2%}",
                  annotation_position="top left")

    # Format x-axis as percentage
    fig.update_layout(
        xaxis=dict(tickformat=".0%", range=[-0.4, 0.4]),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig.to_html(full_html=False)

def render_intraday_contribution_5(selected_sectors=["All"]):
    """
    Shows a single horizontal bar chart with the top 5 and bottom 5
    companies by IntradayContribution. Negative bars = green,
    positive bars = red. Ordered ascending (most negative on bottom).
    """
    df = getQQQMHolding()

    # 1. Filter by sectors unless 'All'
    if "All" not in selected_sectors:
        df = df[df["Sector"].isin(selected_sectors)]

    # 2. Convert IntradayContribution to numeric, drop NaNs
    df["IntradayContribution"] = pd.to_numeric(df["IntradayContribution"], errors="coerce")
    df.dropna(subset=["IntradayContribution"], inplace=True)

    # 3. Sort ascending: most negative is first in the list
    df_sorted = df.sort_values("IntradayContribution")

    # 4. Bottom 5 (lowest) and Top 5 (highest)
    bottom_5 = df_sorted.head(5)
    top_5 = df_sorted.tail(5)

    # 5. Combine them into a single DataFrame
    combined = pd.concat([bottom_5, top_5], ignore_index=True)

    # For each row, create a label like: "NVDA (-0.70%)"
    combined["Label"] = combined["Ticker"] + " (" + (combined["IntradayContribution"] * 100).round(2).astype(str) + "%)"

    # 6. Determine bar colors (negative=red, positive=green)
    bar_colors = []
    for val in combined["IntradayContribution"]:
        if val < 0:
            bar_colors.append("#e74c3c")
        else:
            bar_colors.append("#2ecc71")

    # 7. Build a horizontal bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=combined["IntradayContribution"],  # X values
                y=combined["Label"],                 # Y labels
                orientation="h",
                text=combined["Ticker"],             # For hover text (optional)
                marker=dict(color=bar_colors),
            )
        ]
    )

    # 8. Configure layout
    fig.update_layout(
        #title="Top 5 / Bottom 5 Companies by Intraday Contribution",
        xaxis_title="IntradayContribution",
        yaxis_title="Company",
        margin=dict(l=150, r=50, t=50, b=50),
        plot_bgcolor="white",
        showlegend=False
    )
    # Format x-axis as % 
    fig.update_xaxes(tickformat=".2%")

    return fig.to_html(full_html=False)

# Filter Form (with ticker and name input)
filter_form = dbc.Row(
    [
        dbc.Col(dcc.Input(id="filter-ticker", type="text", placeholder="Ticker", className="form-control"), width=2),
        dbc.Col(dcc.Input(id="filter-name", type="text", placeholder="Name", className="form-control"), width=2),
    ],
    className="mb-3",
)

# 修改更新频率选择 Dropdown：选项改为 "3秒"、"10秒" 和 "不更新"，默认值为 "不更新"
update_speed_dropdown = dbc.Row(
    dbc.Col(
        dcc.Dropdown(
            id="update-speed",
            options=[
                {"label": "3s", "value": "3s"},
                {"label": "10s", "value": "10s"},
                {"label": "No Update", "value": "No Update"}
            ],
            value="No Update",
            clearable=False,
            style={
                "width": "100%",
                "background-color": "#ffffff",  # Set dropdown background to white
                "color": "#000000",  # Set text color to black for the dropdown options
                }
        ),
    ),
    className="mb-3"
)

sector_filter_dropdown = dbc.Row(
    dbc.Col(
        dcc.Dropdown(
            id="filter-sector",
            options=[{"label": "All", "value": "All"}] + [{"label": sec, "value": sec} for sec in [
                'Information Technology', 'Consumer Discretionary', 'Communication Services',
                'Consumer Staples', 'Materials', 'Health Care', 'Industrials', 'Utilities',
                'Financials', 'Energy', 'Real Estate'
            ]],
            value=["All"],  # Default selection can be 'All'
            multi=True,  # Make it multi-select
            clearable=True,  # Allow clearing the selection
            style={
                "width": "100%",
                "background-color": "#ffffff",  # Set dropdown background to white
                "color": "#000000",  # Set text color to black for the dropdown options
                }  # Make the dropdown full-width
        ),
    ),
    className="mb-3"
)

# Sidebar (with multi-select dropdown for sectors and refresh time)
sidebar = [ 
    
    # Title and Link
    html.H1("QuantaTrack", className="mt-3"),
    html.H2("NASDAQ 100 Companies", className="mt-3"),
    html.A(
        "NASDAQ 100 Index ETF", 
        href="https://www.invesco.com/us/financial-products/etfs/product-detail?audienceType=Investor&productId=ETF-QQQM", 
        className="text-primary"
    ),
    
    html.Hr(),  # Optional line separator
    
    # Refresh Time Dropdown
    dbc.Label('Refresh Time'),
    update_speed_dropdown,  # Assuming this is a dropdown for selecting the refresh time

    html.Hr(),  # Optional line separator
    
    # Sector Selector Dropdown
    dbc.Label("Select Sectors"),
    sector_filter_dropdown,
    html.Hr(),  # Optional line separator

    # Footer with Markdown
    html.Footer(
        [
            dcc.Markdown('''
                NASDAQ 100 Tracker is developed by Ethan Fang, Jenny Zhang, Kevin Gao, and Ziyuan Zhao.  
                The application provides dynamic, real-time NASDAQ 100 tracking and visualization to help investors make data-driven decisions with ease.
                Dashboard latest update on DATE         
                [Link to the Github Repo](https://github.com/UBC-MDS/DSCI-532_2025_3_QuantaTrack)  
            ''', 
            style={
                "text-align": "left",  # Center the text
                "font-size": "12px",  # Set appropriate font size
                "background-color": "#343a40",  # Dark background color for sidebar
                "color": "#ffffff",  # Black color for footer text
                "padding-top": "20px",  # Add some padding on top
                "padding-bottom": "10px",  # Add some padding at the bottom
                "padding-left": "10px",  # Add some padding at the bottom
                'flexShrink': 0,  # Prevent footer from shrinking
                'position': 'absolute',  # Position the footer at the bottom
                'bottom': '0',  # Always stick to the bottom
                'left': '0',  # Always stick to the left
                "width": "100%",  # Ensure it takes the full width of the sidebar
                }
            )
        ]
    ),
]

# 保存原始列定义（用于恢复原始表头名称）
original_columns = [
    {"name": col, "id": col, "type": "numeric", "format": {"specifier": ".2%"}}
    if col in [
        'Weight', 'IntradayReturn', 'IntradayContribution','DividendYield', 
        'YTDReturn', 'YTDContribution'
    ]
    else {"name": col, "id": col, "type": "numeric", "format": {"specifier": ".2f"}}
    if col in [
        'Price', 'PE', 'PB', 'Dividend'
    ]
    else {"name": col, "id": col}
    for col in [
        'Ticker', 'Name', 'Weight', 'Price', 'IntradayReturn', 'Volume', 'Amount', 
        'IntradayContribution', 'MarketCap', 'YTDReturn', 'YTDContribution', 'PE', 
        'PB', 'Profit_TTM', 'DividendYield', 'Dividend', 'SharesOutstanding', 
        'Sector', 'Date'
    ]
]

# 数据表格 (Table) 修改：添加自定义排序属性
table = dash_table.DataTable(
    id="stock-table",
    columns=original_columns,
    sort_action="custom",       # 启用自定义排序
    sort_mode="single",         # 单列排序
    style_table={
        "overflowX": "auto",
        "margin": "20px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    },
    style_cell={
        "textAlign": "left",       # 修改为左对齐
        "padding": "12px",         # 增加内边距
        "fontFamily": "Arial, sans-serif",
        "fontSize": "14px",
    },
    style_header={
        "backgroundColor": "#f0f0f0",
        "fontWeight": "bold",
        "border": "1px solid #ccc"
    },
    style_data={
        "backgroundColor": "white",
        "border": "1px solid #ccc"
    },
    style_data_conditional=[],  # 回调将更新该属性
)

# 修改 store_components，新增 data-store 用于存放更新数据
store_components = html.Div([
    dcc.Store(id="sort-state", data={}),
    dcc.Store(id="original-data"),
    dcc.Store(id="data-store")
])

# 新增 dcc.Interval 用于触发数据更新（隐藏组件）
data_update_interval = dcc.Interval(
    id="data-update-interval",
    interval=1000,  # 默认 1秒
    n_intervals=0
)

pie_chart = html.Div(
    id="pie-chart-container", children=[
        html.Iframe(
            srcDoc=render_pie_chart(selected_sectors=["All"]), 
            # style={"border": "0", "width": "100%", "height": "100px"}
        )
    ]
)

scatter_plot = html.Div(
    id="scatter-plot-container", children=[
        html.Iframe(
            srcDoc=render_scatter_plot(selected_sectors=["All"]),  # Default to all sectors
            style={"border": "0", "width": "100%", "height": "100px"}
        )
    ]
)

ytd_dist = html.Div(
    id="ytd-dist-container", children=[
        html.Iframe(
            srcDoc=render_ytd_distribution(selected_sectors=["All"]),
            style={"border": "0", "width": "100%", "height": "100px"}
        )
    ]
)

intraday_cont_5 = html.Div(
    id="intraday-contribution-top5-bottom5-container", children=[
        html.Iframe(
            srcDoc=render_intraday_contribution_5(selected_sectors=["All"]),
            style={"border": "0", "width": "100%", "height": "100px"}
        )
    ]
)

# Download CSV button and component
download_csv = dbc.Col(
    children=[
        dbc.Button("Download CSV", id="download-csv-btn", color="primary", className="mb-3"),
        dcc.Download(id="download-csv")
    ],
    md="auto",  # Automatically adjusts the column width
    className="text-right"  # Right-align the button
)

# Search box
search_box = dbc.Col(filter_form, md=10)  # Adjust size as needed

# Row for the search box and download CSV button on the same line
search_download_row = dbc.Row(
    [
        search_box,
        download_csv
    ],
    align="center"  # Vertically center the items in the row
)


# 页面内容 (Main Content) 修改：使用 html.Iframe 显示 pyecharts 图表
layout = dbc.Container(
    [
        # Row for Global Filters (Refresh Time)
        dbc.Row(
            [
                dbc.Col(
                    sidebar, md=2, 
                    style={
                        # 'display': 'flex',
                        #'flexDirection': 'column',  # Stack children vertically
                        'position': 'fixed',  # Fix the sidebar on the left
                        'top': '0',  # Make sure it starts at the top of the page
                        'left': '0',  # Fix it to the left of the page
                        'minHeight': '100vh',  # Ensure the sidebar takes full height of the page
                        'overflowY': 'auto',  # Allow the sidebar to scroll if content exceeds viewport height
                        'padding-left': 10,
                        'color': 'white', 
                        'backgroundColor': "#343a40", 
                        "box-sizing": "border-box",  # Include padding and borders in element's total width and height
                        }
                    ),

                # Row for the graphs (Pie chart, Intraday Contribution, etc.)
                dbc.Col(
                    [
                        # Row for Pie chart and Intraday Contribution
                        dbc.Row([
                            dbc.Col(pie_chart), 
                            dbc.Col(intraday_cont_5)
                            ]),
                        # Row for Dividend Yield vs PE and YTD Distribution
                        dbc.Row([
                            dbc.Col(scatter_plot), 
                            dbc.Col(ytd_dist)
                            ]),

                        # Row for Search box and Download CSV button
                        search_download_row,

                        # Screener table row at the bottom
                        dbc.Row(dbc.Col(table)),
                        
                        store_components,  # 添加排序状态与原始数据存储
                        data_update_interval  # 新增 Interval 控件，用于周期更新
                    ],
                    md=10,
                    style={
                        'margin-left': '16.67%',  # Adjust for sidebar width (md=2 takes 16.67%)
                    }
                ),
            ]    
        ),
    ],
    fluid=True,  # Ensure the layout is fluid and stretches to the full width of the viewport
)

# 回调函数：根据表头点击循环更新排序状态和箭头显示
@callback(
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
    # 初始化原始数据
    if not original_data:
        original_data = data
    
    # 决定要操作的排序列
    if sort_by:
        sort_col = sort_by[0]["column_id"]
    else:
        # 如果没有新的 sort_by，但已有上次点击记录，则使用它
        sort_col = sort_state.get("last_sorted")
        if not sort_col:
            return data, original_columns, sort_state, original_data, sort_by

    # 根据上一次状态计算新的排序方向
    prev = sort_state.get(sort_col, "none")
    if prev == "none":
        new_direction = "asc"
    elif prev == "asc":
        new_direction = "desc"
    else:
        new_direction = "none"
    # 重置排序状态，并记录当前点击列
    sort_state = {col_def["id"]: "none" for col_def in original_columns}
    sort_state["last_sorted"] = sort_col
    sort_state[sort_col] = new_direction

    # 更新列标题，添加箭头提示
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

    # 更新数据：若方向为 "none" 恢复原始，否则排序数据
    if new_direction == "none":
        sorted_data = original_data
        sort_by = []  # 清空排序状态
    else:
        reverse = True if new_direction == "desc" else False
        sorted_data = sorted(data, key=lambda row: row.get(sort_col, None), reverse=reverse)

    return sorted_data, new_columns, sort_state, original_data, sort_by
