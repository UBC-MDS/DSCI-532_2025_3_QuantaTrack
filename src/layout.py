import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, callback, Input, Output, State
from src.plotting import *

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
                The application provides dynamic, real-time NASDAQ 100 tracking to help investors make data-driven decisions with ease.  
                Latest update on Mar. 1, 2025.  
                [Link to the Github Repo](https://github.com/UBC-MDS/DSCI-532_2025_3_QuantaTrack)  
            ''', 
            style={
                "text-align": "left",  # Center the text
                "font-size": "15px",  # Set appropriate font size
                "background-color": "#343a40",  # Dark background color for sidebar
                "color": "#ffffff",  # Black color for footer text
                "padding": "10px",  # Add some padding 
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

# Components for Visualization
pie_chart = html.Div(
    id="pie-chart-container", children=[
        html.Iframe(
            srcDoc=render_pie_chart(selected_sectors=["All"]), 
            style={"border": "0", "width": "100%", "height": "100px"}
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

# Table components
# Save original column definitions (used for restoring the original table header names)
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

# Data table (Table) modification: Add custom sorting properties
table = dash_table.DataTable(
    id="stock-table",
    columns=original_columns,
    sort_action="custom",       # Enable custom sorting
    sort_mode="single",         # Single column sorting
    style_table={
        "overflowX": "auto",
        "margin": "20px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    },
    style_cell={
        "textAlign": "left",       # Change to left alignment
        "padding": "12px",         # Add padding
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
    style_data_conditional=[],  # This will be updated by the callback
)

# Modify store_components, add data-store to store updated data
store_components = html.Div([
    dcc.Store(id="sort-state", data={}),
    dcc.Store(id="original-data"),
    dcc.Store(id="data-store")
])

# Add dcc.Interval to trigger data updates (hidden component)
data_update_interval = dcc.Interval(
    id="data-update-interval",
    interval=1000,  # Default 1 second
    n_intervals=0
)


# Main content container
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
                            ], 
                            class_name="g-0",
                            align="start"
                        ),
                        # Row for Dividend Yield vs PE and YTD Distribution
                        dbc.Row([
                            dbc.Col(scatter_plot), 
                            dbc.Col(ytd_dist)
                            ],
                            class_name="g-0",
                            align="end"
                        ),

                        # Row for Search box and Download CSV button
                        search_download_row,

                        # Screener table row at the bottom
                        dbc.Row(dbc.Col(table)),
                        
                        store_components,  # Add sorting state and original data storage
                        data_update_interval  # Add Interval component for periodic updates
                    ],
                    md=10,
                    class_name="g-0",
                    style={
                        'margin-left': '16.67%',  # Adjust for sidebar width (md=2 takes 16.67%)
                    }
                ),
            ]    
        ),
    ],
    fluid=True,  # Ensure the layout is fluid and stretches to the full width of the viewport
)

