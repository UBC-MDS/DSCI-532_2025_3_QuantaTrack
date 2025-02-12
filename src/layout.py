import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

# 侧边栏 (Sidebar)
sidebar = html.Div(
    [
        html.H5("US", className="text-muted"),
        html.Ul(
            [
                html.Li(dbc.NavLink("NASDAQ 100", active=True, href="#")),
                html.Li("S&P 500"),
            ]
        ),
    ],
    className="sidebar p-3",
    style={"width": "200px", "height": "100vh", "position": "fixed", "left": "0", "top": "0", "background": "#f8f9fa"},
)

# 筛选条件 (Filter Criteria)
filter_form = dbc.Row(
    [
        dbc.Col(dcc.Input(id="filter-ticker", type="text", placeholder="Ticker", className="form-control"), width=2),
        dbc.Col(dcc.Input(id="filter-name", type="text", placeholder="Name", className="form-control"), width=3),
        dbc.Col(dcc.Dropdown(
            id="filter-sector",
            options=[{"label": "All", "value": "All"}] + [{"label": sec, "value": sec} for sec in ["Tech", "Consumer"]],
            value="All",
            clearable=False
        ), width=2),
    ],
    className="mb-3",
)

# 数据表格 (Table)
table = dash_table.DataTable(
    id="stock-table",
    columns=[
        {"name": col, "id": col} for col in ["Ticker", "Name", "Weight", "Price", "IntradayReturn", "Volume", "Amount", "MarketCap", "YTDReturn"]
    ],
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "left"},
)

# 页面内容 (Main Content)
content = html.Div(
    [
        html.H2("NASDAQ 100 Companies", className="mt-3"),
        html.A("NASDAQ 100 Index ETF", href="#", className="text-primary"),
        dbc.Checkbox(id="show-charts", label="Show Charts", value=False),
        html.Div("Filter Criteria", className="text-muted"),
        filter_form,
        table,
    ],
    style={"margin-left": "220px", "padding": "20px"},
)

# 组合完整布局
layout = html.Div([sidebar, content])
