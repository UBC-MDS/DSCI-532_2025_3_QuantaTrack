import pandas as pd
import numpy as np

from pyecharts.charts import Pie
import plotly.graph_objects as go
import plotly.express as px
from pyecharts import options as opts
from src.qqqm_data import getQQQMHolding
from src.xueqiu_data import getUSStockHistoryByDate

# A dictionary mapping each NASDAQ 100 sector to a specific color
SECTOR_COLORS = {
    "Information Technology": "#1f78b4",
    "Communication Services": "#33a02c",
    "Consumer Discretionary": "#e31a1c",
    "Consumer Staples": "#ff7f00",
    "Materials": "#6a3d9a",
    "Health Care": "#b15928",
    "Industrials": "#a6cee3",
    "Utilities": "#b2df8a",
    "Financials": "#fb9a99",
    "Energy": "#fdbf6f",
    "Real Estate": "#cab2d6",
    "Other": "#cccccc"  # fallback for any sector not listed
}

def render_pie_chart(selected_sectors=["All"]):
    """
    Generates a doughnut chart displaying the weight distribution 
    of companies in the selected sectors, coloring slices by sector.
    """
    _df = getQQQMHolding()

    # Treat an empty selection the same as ["All"]
    if not selected_sectors:
        selected_sectors = ["All"]

    # If 'All' is selected, group by sector
    if "All" in selected_sectors:
        df_sector = _df.groupby('Sector', as_index=False)["Weight"].sum()
        df_sector = df_sector.sort_values("Weight", ascending=False)
        chart_title = "NASDAQ 100 by Sector"

        # Build data_pairs from sector & weight
        data_pairs = list(zip(df_sector["Sector"], df_sector["Weight"]))

        # Build a color_list by referencing each row's Sector
        color_list = []
        for _, row in df_sector.iterrows():
            sector_name = row["Sector"]
            color_list.append(SECTOR_COLORS.get(sector_name, SECTOR_COLORS["Other"]))

    else:
        # Filter df by the chosen sectors
        _df = _df[_df["Sector"].isin(selected_sectors)]

        # Sort by weight descending, then pick top 10
        df_sorted = _df.sort_values("Weight", ascending=False)
        top_10 = df_sorted.head(10).copy()
        rest = df_sorted.iloc[10:].copy()

        # Create a row for 'Other Companies'
        rest_combined = pd.DataFrame({
            "Name": ["Other Companies"],
            "Weight": [rest["Weight"].sum()],
            "Sector": ["Other"]  # fallback sector label
        })

        # Combine top_10 with the "other" row
        # (Ensure top_10 has a 'Sector' column as well)
        top_10 = top_10[["Name", "Weight", "Sector"]]  # keep relevant columns
        combined_df = pd.concat([top_10, rest_combined], ignore_index=True)

        chart_title = "Top 10 Companies (Selected Sectors)"

        # Convert to a list of (company_name, weight) for pyecharts
        data_pairs = list(zip(combined_df["Name"], combined_df["Weight"]))

        # Build a color list by each company's sector
        color_list = []
        for _, row in combined_df.iterrows():
            sec = row["Sector"]
            color_list.append(SECTOR_COLORS.get(sec, SECTOR_COLORS["Other"]))

    # Create a doughnut chart with pyecharts
    chart = (
        Pie(init_opts=opts.InitOpts(width="590px", height="300px"))
        .add(
            series_name="",
            data_pair=data_pairs,
            radius=["30%", "70%"],
            center=["50%", "50%"]
        )
        .set_colors(color_list)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=chart_title,
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=18,
                    color="black",
                    font_family="Calibri",
                    font_weight="bold"
                )
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {d}%")
        )
    )

    return chart.render_embed()

# Function to render the scatter plot based on selected sectors
def render_scatter_plot(selected_sectors):
    """
    Renders a scatter plot of Dividend Yield vs. PE for selected sectors, 
    color-coded by sector, with tooltips displaying company details.

    Parameters
    ----------
    selected_sectors : list of str
        A list of sectors to filter the data by. If empty or "All" is provided, 
        no filtering is applied and all sectors are included.

    Returns
    -------
    str
        HTML representation of the Plotly scatter plot figure.
    
    Notes
    -----
    - The plot will display the Dividend Yield vs. PE for each company.
    - The colors of the points are determined by the sector of the company.
    - Tooltips will show detailed information for each company such as its ticker, name, 
      sector, Dividend Yield, and PE ratio.
    - If no sectors are provided, all sectors are included by default.
    """
    # 1. Get and process data
    _df = getQQQMHolding()

    # 2. If there are selected sectors, filter data based on them
    selected_sectors = selected_sectors or ["All"]
    if "All" not in selected_sectors:  # Only filter if "All" is not selected
        _df = _df[_df["Sector"].isin(selected_sectors)]  # Filter by selected sectors

    # 3. Clean and prepare data
    scatter_data = []
    for index, row in _df.iterrows():
        if pd.notna(row['DividendYield']) and pd.notna(row['PE']):  # Only take rows with valid values
            scatter_data.append(
                {
                    "x": row['PE'],  # X-axis: PE (Forward PE or other PE)
                    "y": row['DividendYield'],  # Y-axis: Dividend Yield
                    "text": f"{row['Ticker']} - {row['Name']}<br>Sector = {row['Sector']}<br>Dividend Yield = {row['DividendYield'] * 100:.2f}%<br>PE = {row['PE']}",  # Tooltip with Sector
                    "name": row['Name'],  # Display company name in legend (if needed)
                    "sector": row['Sector']  # Store sector information for color coding
                }
            )

    # 4. Create Plotly scatter plot
    fig = go.Figure()

    # Create a color map for sectors
#    unique_sectors = _df['Sector'].unique()  # Get unique sectors
#    sector_to_color = {sector: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] 
#                       for i, sector in enumerate(unique_sectors)}  # Map sector to a color using a color palette

    # 5. Create Plotly scatter plot
    fig = go.Figure()

    # Add data points to the figure, color by sector
    for data in scatter_data:
        color_used = SECTOR_COLORS.get(data['sector'], SECTOR_COLORS["Other"])
        fig.add_trace(go.Scatter(
            x=[data['x']],
            y=[data['y']],
            mode='markers',
            text=data['text'],
            marker=dict(size=10, color=color_used)
        ))

    # 5. Update layout
    fig.update_layout(
        width=590,
        height=300,
        title="Dividend Yield vs. PE",
        title_font=dict(size=18, color="black", family="Calibri", weight="bold"),
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
            linecolor='gray'  # Outer line color for the x-axis
        ),
        yaxis=dict(
            showgrid=True,  # Show grid lines
            zeroline=True,  # Show zero line
            gridcolor='rgba(0, 0, 0, 0.1)',  # Light gray grid lines
            showline=True,  # Show outer axis line (border)
            linewidth=1,  # Reduced border thickness for the y-axis
            linecolor='gray',  # Outer line color for the y-axis
            tickformat=".2%",  # Format the ticks as percentages
        ),
        # Full border around the whole chart
        margin=dict(l=50, r=50, t=40, b=10),  # Add margins to ensure full border
        shapes=[
            dict(
                type="rect",  # Shape type is rectangle
                x0=0, x1=1, y0=0, y1=1,  # Full area of the plot
                xref="paper", yref="paper",  # Reference to paper coordinates (entire figure)
                line=dict(color="gray", width=1)  # Gray border with thinner thickness
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
        title="YTD Return Distribution", 
        opacity=0.5
    )
    fig.update_traces(name="YTDReturn")
    
    # # Add kernel density for smooth curve
    # fig.add_trace(
    #     px.histogram(df, x="YTDReturn", nbins=20, histnorm="probability density").data[0]
    # )
    # fig.data[1].marker = dict(opacity=0)  # Hide second histogram bars, keep the curve
    # fig.data[1].line = dict(color="blue", width=2)

    # Calculate mean & median
    mean_val = df["YTDReturn"].mean()
    median_val = df["YTDReturn"].median()

    # Add lines for mean (green) & median (red)
    fig.add_vline(x=mean_val, line_width=2, line_dash="dash", line_color="darkblue")
    fig.add_vline(x=median_val, line_width=2, line_dash="solid", line_color="darkblue")

    max_count = 0
    if fig.data and hasattr(fig.data[0], "y") and fig.data[0].y is not None:
        max_count = max(fig.data[0].y)

    # 4) Add two line traces for Mean & Median
    #    (These lines will appear in the legend)
    fig.add_trace(
        go.Scatter(
            x=[mean_val, mean_val],
            y=[0, max_count],
            mode='lines',
            line=dict(color='darkblue', width=2, dash='dash'),
            name=f"Mean: {mean_val:.2%}"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[median_val, median_val],
            y=[0, max_count],
            mode='lines',
            line=dict(color='darkblue', width=2, dash='solid'),
            name=f"Median: {median_val:.2%}"
        )
    )

    # Format x-axis as percentage
    fig.update_layout(
        width=590,
        height=300,
        title_font=dict(size=18, color="black", family="Calibri", weight="bold"),
        title_x=0.5,
        showlegend=True,
        legend=dict(
            x=0,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.8)'  # optional: white background behind legend
        ),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='gray',
            tickformat=".0%",
            title="YTD Return"
        ),
        yaxis=dict(
        title="Count"
        ),
        barmode='overlay',
        margin=dict(l=50, r=50, t=40, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
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
    
    if len(df_sorted) <= 10:
        combined = df_sorted
    else:
        bottom_5 = df_sorted.head(5)
        top_5 = df_sorted.tail(5)
        combined = pd.concat([bottom_5, top_5], ignore_index=True)

    # For each row, create a label like: "NVDA (-0.70%)"
    combined["Label"] = combined["Ticker"] + " (" + (combined["IntradayContribution"] * 100).round(2).astype(str) + "%)"

    # 6. Determine bar colors (negative=red, positive=green)
    bar_colors = []
    for val in combined["IntradayContribution"]:
        if val < 0:
            bar_colors.append("#BB4444")
        else:
            bar_colors.append("#A8C089")

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
        width=590,
        height=300,
        title="Companies by Intraday Contribution",
        title_font=dict(size=18, color="black", family="Calibri", weight="bold"),
        title_x=0.5,
        xaxis_title="Intraday Contribution",
        yaxis_title="Company",
        xaxis=dict(
            showline=True,  # Show outer axis line (border)
            linewidth=1,  # Reduced border thickness for the x-axis
            linecolor='gray',  # Outer line color for the x-axis
            tickformat=".2%"
            ),
        # yaxis=dict(
        #     showline=True,  # Show outer axis line (border)
        #     linewidth=1,  # Reduced border thickness for the y-axis
        #     linecolor='gray',  # Outer line color for the y-axis
        #     ),
        margin=dict(l=150, r=50, t=40, b=10),
        plot_bgcolor="white",
        showlegend=False
    )

    return fig.to_html(full_html=False)

def calculate_beta(stock_returns, index_returns):
    """Calculate the beta value"""
    covariance = np.cov(stock_returns, index_returns)[0, 1]
    variance = np.var(index_returns)
    beta = covariance / variance
    return beta


def fetch_stock_data(selected_stock, start_date, end_date):

    stock_data = getUSStockHistoryByDate(selected_stock, start_date, end_date)
    stock_data = stock_data[['Timestamp_str', 'percent', 'close']]  # Keep only the desired columns
    stock_data = stock_data.rename(columns={'Timestamp_str': 'Date', 'percent': 'return', 'close': 'price'})  # Rename columns
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Parse dates
    stock_data.set_index('Date', inplace=True)
    stock_returns = stock_data['return'].dropna() * 100
        
    nasdaq_data = getUSStockHistoryByDate('QQQ', start_date, end_date)
    nasdaq_data = nasdaq_data[['Timestamp_str', 'percent', 'close']]  # Keep only the desired columns
    nasdaq_data = nasdaq_data.rename(columns={'Timestamp_str': 'Date', 'percent': 'return', 'close': 'price'})  # Rename columns
    nasdaq_data['Date'] = pd.to_datetime(nasdaq_data['Date'])  # Parse date
    nasdaq_data.set_index('Date', inplace=True)
    nasdaq_returns = nasdaq_data['return'].dropna() * 100

    return stock_data, nasdaq_data, stock_returns, nasdaq_returns

def render_regression_graph(selected_stock, start_date, end_date):

    stock_data, nasdaq_data, stock_returns, nasdaq_returns = fetch_stock_data(selected_stock, start_date, end_date)

    beta = calculate_beta(stock_returns, nasdaq_returns)

    regression_fig = px.scatter(
            x=nasdaq_returns,
            y=stock_returns,
            trendline="ols",
            labels={'x': 'NASDAQ 100 Returns', 'y': f'{selected_stock} Returns'},
            title=(
                f"Regression Analysis: <b>Beta = {beta: .2f}</b>"
                "<br><span style='font-size:12px; color:gray;'>"
                "Beta represents the sensitivity of the stock's returns to the overall market. Beta = Cov(R<sub>s</sub>, R<sub>m</sub>) / Var(R<sub>m</sub>)"
                "</span>"
            )
        )

    return regression_fig.to_html(full_html=False)

def render_trend_graph(selected_stock, start_date, end_date):

    stock_data, nasdaq_data, stock_returns, nasdaq_returns = fetch_stock_data(selected_stock, start_date, end_date)
    stock_price_normalized = stock_data['price'].dropna() / stock_data['price'].iloc[0]
    nasdaq_price_normalized = nasdaq_data['price'].dropna() / nasdaq_data['price'].iloc[0]
    combined_data = pd.DataFrame({
        'Date': stock_price_normalized.index,  # 日期索引
        'Stock Price': stock_price_normalized,  # 归一化后的股票价格
        'NASDAQ Price': nasdaq_price_normalized  # 归一化后的指数价格
    })

        # 绘制价格走势图
    price_trend_fig = px.line(
        combined_data,  # 数据
        x='Date',  # X 轴：日期
        y=['Stock Price', 'NASDAQ Price'],  # Y 轴：股票和指数价格
        labels={'value': 'Normalized Price', 'variable': 'Legend'},  # 标签
        title=f'{selected_stock} and NASDAQ 100 Price Trend (Normalized)'  # 标题
    )

    return price_trend_fig.to_html(full_html=False)