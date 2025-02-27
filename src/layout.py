import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback, Input, Output, State
import pandas as pd

from pyecharts.charts import Pie
import plotly.graph_objects as go
import plotly.express as px
from pyecharts import options as opts
from qqqm_data import getQQQMHolding


def render_pie_chart():
    # 1. 获取并处理数据
    _df = getQQQMHolding()
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
        "#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE",
        "#3BA272", "#FC8452", "#9A60B4", "#EA7CCC", "#4A90E2","#999999"]

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

# Sidebar (with multi-select dropdown for sectors)
sidebar = html.Div(
    [
        html.H5("US", className="text-muted"),
        html.Ul(
            [
                html.Li(dbc.NavLink("NASDAQ 100", active=True, href="#")),
                #html.Li("S&P 500"),
            ]
        ),
        html.Hr(),  # Optional line separator
        html.H6("Select Sectors", className="text-muted"),  # Title for the dropdown
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
                style={"width": "100%"}  # Make the dropdown full-width
            ),
            style={"padding-top": "10px"}
        ),
    ],
    className="sidebar p-3",
    style={"width": "300px", "height": "100vh", "position": "fixed", "left": "0", "top": "0", "background": "#f8f9fa"},
)

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
            style={"width": "150px"}
        ),
        width="auto"
    ),
    className="mb-3"
)

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

# 页面内容 (Main Content) 修改：使用 html.Iframe 显示 pyecharts 图表
content = html.Div(
    [
        html.H1("NASDAQ 100 Companies", className="mt-3"),
        html.A("NASDAQ 100 Index ETF", href="https://www.invesco.com/us/financial-products/etfs/product-detail?audienceType=Investor&productId=ETF-QQQM", className="text-primary"),
        # 使用 Iframe 显示 pyecharts 渲染的图表
        html.Iframe(srcDoc=render_pie_chart(), 
                    style={"border": "0", "width": "100%", "height": "600px"}),
        # Using Iframe to display the Plotly scatter plot
        html.Div(id="scatter-plot-container", children=[
            html.Iframe(
                srcDoc=render_scatter_plot(selected_sectors=["All"]),  # Default to all sectors
                style={"border": "0", "width": "100%", "height": "600px"}
            )
        ]),
        html.Div("Refresh Time", className="text-muted"),
        update_speed_dropdown,  # 新增更新频率选择控件
        html.Div("Filter Criteria", className="text-muted"),
        filter_form,
        # 新增下载 CSV 按钮和下载组件
        dbc.Button("Download CSV", id="download-csv-btn", color="primary", className="mb-3"),
        dcc.Download(id="download-csv"),
        table,
        store_components,  # 添加排序状态与原始数据存储
        data_update_interval  # 新增 Interval 控件，用于周期更新
    ],
    style={"margin-left": "320px", "padding": "20px"},
)

# 组合完整布局
layout = html.Div([sidebar, content])

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
