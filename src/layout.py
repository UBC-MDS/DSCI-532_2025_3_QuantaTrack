import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_ag_grid import AgGrid
from src.components import *
from src.qqqm_data import getQQQMHolding

nasdaq100_tickers = getQQQMHolding()
latest_update_date = nasdaq100_tickers['Date'].iloc[0] if not nasdaq100_tickers.empty else "N/A"

# 定义所有表格列配置，供表格和下拉菜单使用
all_columns = [
    {"field": "Ticker"},
    {"field": "Name"},
    {"field": "Weight", "valueFormatter": {"function": "(params.value * 100).toFixed(2) + '%'"}},
    {"field": "Price", "valueFormatter": {"function": "params.value.toFixed(2)"}},
    {
        "field": "IntradayReturn",
        "valueFormatter": {"function": "(params.value * 100).toFixed(2) + '%'"},
        "cellStyle": {
            "function": "params.value ? {'backgroundColor': 'rgba(' + (params.value < 0 ? '255,0,0' : '0,255,0') + ',' + Math.min(Math.abs(params.value) / 0.1, 1) + ')'} : null"
        }
    },
    {"field": "Volume", "valueFormatter": {"function": "(params.value / 1e6).toFixed(2) + 'M'"}},
    {"field": "Amount", "valueFormatter": {"function": "(params.value / 1e9).toFixed(2) + 'B'"}},
    {"field": "IntradayContribution", "valueFormatter": {"function": "(params.value * 100).toFixed(2) + '%'" }},
    {"field": "MarketCap", "valueFormatter": {"function": "(params.value / 1e9).toFixed(2) + 'B'"}},
    {
        "field": "YTDReturn",
        "valueFormatter": {"function": "(params.value * 100).toFixed(2) + '%'"},
        "cellStyle": {
            "function": "params.value ? {'backgroundColor': 'rgba(' + (params.value < 0 ? '255,0,0' : '0,255,0') + ',' + Math.min(Math.abs(params.value) / 0.5, 1) + ')'} : null"
        }
    },
    {"field": "YTDContribution", "valueFormatter": {"function": "(params.value * 100).toFixed(2) + '%'" }},
    {"field": "PE", "valueFormatter": {"function": "params.value.toFixed(2)"}},
    {"field": "PB", "valueFormatter": {"function": "params.value.toFixed(2)"}},
    {"field": "Profit_TTM", "valueFormatter": {"function": "(params.value / 1e9).toFixed(2) + 'B'"}},
    {"field": "DividendYield", "valueFormatter": {"function": "(params.value * 100).toFixed(2) + '%'" }},
    {"field": "Dividend", "valueFormatter": {"function": "params.value.toFixed(2)"}},
    {"field": "SharesOutstanding", "valueFormatter": {"function": "(params.value / 1e9).toFixed(2) + 'B'"}},
    {"field": "Sector"},
    {"field": "Date"},
]

# 修改更新频率下拉框
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
                "background-color": "#ffffff",
                "color": "#000000",
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
            value=["All"],
            multi=True,
            clearable=True,
            style={
                "width": "100%",
                "background-color": "#ffffff",
                "color": "#000000",
            }
        ),
    ),
    className="mb-3"
)

# Sidebar 定义
sidebar = [
    html.H1("QuantaTrack", className="mt-3"),
    html.H2("NASDAQ 100 Companies", className="mt-3"),
    html.A(
        "NASDAQ 100 Index ETF", 
        href="https://www.invesco.com/us/financial-products/etfs/product-detail?audienceType=Investor&productId=ETF-QQQM", 
        style={"color": "yellow"}
    ),
    html.Hr(),
    dbc.Label('Refresh Time'),
    update_speed_dropdown,
    html.Hr(),
    dbc.Label("Select Sectors"),
    sector_filter_dropdown,
    html.Hr(),
    html.Footer(
        [
            dcc.Markdown(f'''
                NASDAQ 100 Tracker is developed by Ethan Fang, Jenny Zhang, Kevin Gao, and Ziyuan Zhao.  
                The application provides dynamic, real-time NASDAQ 100 tracking to help investors make data-driven decisions with ease.\n  
                Latest update on {latest_update_date}.  
                [Link to the Github Repo](https://github.com/UBC-MDS/DSCI-532_2025_3_QuantaTrack)  
            ''', 
            style={
                "text-align": "left",
                "font-size": "15px",
                "background-color": "#343a40",
                "color": "#ffffff",
                "padding": "10px",
                'flexShrink': 0,
                'position': 'absolute',
                'bottom': '0',
                'left': '0',
                "width": "100%",
                }
            )
        ]
    ),
]

# Components for Visualization
pie_chart = html.Div(
    id="pie-chart-container", children=[
        html.Iframe(
            srcDoc=render_pie_chart(selected_sectors=["All"]), 
            style={"border": "0", "width": "100%", "height": "350px"}
        )
    ]
)

scatter_plot = html.Div(
    id="scatter-plot-container", children=[
        html.Iframe(
            srcDoc=render_scatter_plot(selected_sectors=["All"]),  # Default to all sectors
            style={"border": "0", "width": "100%", "height": "350px"}
        )
    ]
)

ytd_dist = html.Div(
    id="ytd-dist-container", children=[
        html.Iframe(
            srcDoc=render_ytd_distribution(selected_sectors=["All"]),
            style={"border": "0", "width": "100%", "height": "350px"}
        )
    ]
)

intraday_cont_5 = html.Div(
    id="intraday-contribution-top5-bottom5-container", children=[
        html.Iframe(
            srcDoc=render_intraday_contribution_5(selected_sectors=["All"]),
            style={"border": "0", "width": "100%", "height": "350px"}
        )
    ]
)

# Components for stock analysis
regression_graph = html.Div(
    id="regression-graph-container", children=[
        html.Iframe(
            srcDoc=render_regression_graph(selected_stock='AAPL', start_date='2024-01-01', end_date='2025-01-01'), 
            style={"border": "0", "width": "100%", "height": "350px"}
        )
    ]
)

price_trend_graph = html.Div(
    id="price-trend-graph-container", children=[
        html.Iframe(
            srcDoc=render_trend_graph(selected_stock='AAPL', start_date='2024-01-01', end_date='2025-01-01'), 
            style={"border": "0", "width": "100%", "height": "350px"}
        )
    ]
)

# Filter Form (with ticker and name input)
filter_form = dbc.Row(
    [
        dbc.Col(dcc.Input(id="filter-ticker", type="text", placeholder="Ticker", className="form-control"), width=2),
        dbc.Col(dcc.Input(id="filter-name", type="text", placeholder="Name", className="form-control"), width=2),
    ],
    className="mb-3",
)

# Search box component
search_box = dbc.Col(filter_form, md=10)  # Adjust size as needed

# Download CSV button and component
download_csv = dbc.Col(
    children=[
        dbc.Button("Download CSV", id="download-csv-btn", color="primary", className="mb-3"),
        dcc.Download(id="download-csv")
    ],
    md="auto",  # Automatically adjusts the column width
    className="text-right"  # Right-align the button
)

# Row for the search box and download CSV button on the same line
search_download_row = dbc.Row(
    [
        search_box,
        download_csv
    ],
    justify="between",  
)

# 修改自定义表格列选择组件，添加 "Column Select " 标签到下拉菜单左边
column_selector = dbc.Row([
    dbc.Col(html.Label("Select Column"), width="auto"),
    dbc.Col(
        dcc.Dropdown(
            id="column-selector",
            options=[{"label": col["field"], "value": col["field"]} for col in all_columns],
            value=[col["field"] for col in all_columns[:5]],    # 默认选中前5列
            multi=True,
            clearable=False,
            style={"width": "100%"}
        ),
        width=True
    )
], className="mb-3")

# dash ag grid 表格组件，使用全局变量 all_columns 作为初始列配置
table = AgGrid(
    id="stock-table",
    columnDefs=all_columns,
    rowData=[],  # 初始数据为空
    defaultColDef={'filter': True},
    style={"height": 600},
    dashGridOptions={"pagination": True, "paginationAutoPageSize": True},
)

# Modify store_components, add data-store to store updated data
store_components = html.Div([
    dcc.Store(id="data-store")
])

# Add dcc.Interval to trigger data updates (hidden component)
data_update_interval = dcc.Interval(
    id="data-update-interval",
    interval=1000,  # Default 1 second
    n_intervals=0
)


## 生成下拉菜单选项
stock_dropdown_options = [
    {'label': nasdaq100_tickers.iloc[i]['Name'], 'value': nasdaq100_tickers.iloc[i]['Ticker']}
    for i in range(len(nasdaq100_tickers))
]

tabs = dbc.Tabs([
    dbc.Tab(
        [
            dbc.Row([
                dbc.Col(pie_chart), 
                dbc.Col(intraday_cont_5)
            ], class_name="g-0", style={"marginTop": "20px"}),
            dbc.Row([
                dbc.Col(ytd_dist), 
                dbc.Col(scatter_plot)
            ], class_name="g-0"),
        ],
        label="Overview"
    ),

    dbc.Tab(
        [
            dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='stock-dropdown',
                    options=[],
                    value=None,  # 默认值
                    placeholder="Select a stock",  # 提示文本
                ),
                width=6,
            ),
            dbc.Col(
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=pd.to_datetime('2024-01-01'),
                    end_date=pd.to_datetime('2025-02-05'),
                    display_format='YYYY-MM-DD',  # 日期格式
                    min_date_allowed=pd.to_datetime('2010-01-01'),
                    max_date_allowed=pd.to_datetime('2025-12-31'),
                ),
                width=6,
            ),
        ]),
            dbc.Row([
                dbc.Col(regression_graph),
                dbc.Col(price_trend_graph)
            ], class_name="g-0", style={"marginTop": "20px"}),
        ],
        label="Stock"
    ),
    
    dbc.Tab(
        [
            # 将自定义表格列选择组件添加到 Data 页签
            column_selector,
            search_download_row,
            dbc.Row(dbc.Col(table)),
        ],
        label="Data"
    )
])

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    sidebar, md=2,
                    style={
                        'position': 'fixed',
                        'top': '0',
                        'left': '0',
                        'minHeight': '100vh',
                        'overflowY': 'auto',
                        'padding-left': 10,
                        'color': 'white', 
                        'backgroundColor': "#343a40", 
                        "box-sizing": "border-box",
                        }
                    ),
                dbc.Col(
                    [
                        tabs, 
                        store_components,
                        data_update_interval
                    ],
                    md=10,
                    class_name="g-0",
                    style={
                        'margin-left': '16.67%',
                    }
                ),
            ]    
        ),
    ],
    fluid=True
)

