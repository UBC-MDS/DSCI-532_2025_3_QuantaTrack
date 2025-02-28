import pandas as pd

from pyecharts.charts import Pie
import plotly.graph_objects as go
import plotly.express as px
from pyecharts import options as opts
from src.qqqm_data import getQQQMHolding

def render_pie_chart(selected_sectors=["All"]):
    # 1. 获取并处理数据
    _df = getQQQMHolding()
    
    # Treat an empty selection the same as ["All"]
    if not selected_sectors:
        selected_sectors = ["All"]

    if "All" in selected_sectors:
        df_sector = _df.groupby('Sector', as_index=False)["Weight"].sum()
        df_sector = df_sector.sort_values("Weight", ascending=False)
        data_pairs = list(zip(df_sector["Sector"], df_sector["Weight"]))
        chart_title = "NASDAQ 100 by Sector"
 
    else:
        # 2) Filter df by the chosen sectors
        _df = _df[_df["Sector"].isin(selected_sectors)]

        # Sort by weight descending, top 10
        df_sorted = _df.sort_values("Weight", ascending=False)
        top_10 = df_sorted.head(10)
        # Combine the "other" leftover if needed
        rest = df_sorted.iloc[10:]
        rest_combined = pd.DataFrame({
            "Name": ["Other Companies"], 
            "Weight": [rest["Weight"].sum()]
        })
        combined_df = pd.concat([top_10, rest_combined], ignore_index=True)
        
        # Convert to a list of (company, weight)
        data_pairs = list(zip(combined_df["Name"], combined_df["Weight"]))
        chart_title = "Top 10 Companies (Selected Sectors)"

    # 3. 为前 10 项指定不同颜色
    colors= [
        "#08306b", "#08519c", "#2171b5", "#4292c6", "#6baed6",
        "#9ecae1", "#c6dbef", "#deebf7", "#f7fbff", "#cccccc"]

    # 4. 创建环形图
    chart = (
        Pie(init_opts=opts.InitOpts(width="600px", height="500px"))
        .add(
            series_name="",
            data_pair=data_pairs,
            radius=["30%", "70%"],  # 环形图的内外半径
            center=["50%", "50%"]   # 图表居中
        )
        .set_colors(colors)  # 为每个扇区设置颜色
        .set_global_opts(
            title_opts=opts.TitleOpts(title=chart_title, pos_left="center"),
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
                    "text": f"{row['Ticker']} - {row['Name']}<br>Sector = {row['Sector']}<br>Dividend Yield = {row['DividendYield'] * 100:.2f}%<br>PE = {row['PE']}",  # Tooltip with Sector
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
        margin=dict(l=50, r=50, t=50, b=50),  # Add margins to ensure full border
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
    fig.add_vline(x=mean_val, line_width=2, line_dash="solid", line_color="green",
                  annotation_text=f"Mean: {mean_val:.2%}",
                  annotation_position="top right")
    fig.add_vline(x=median_val, line_width=2, line_dash="solid", line_color="red",
                  annotation_text=f"Median: {median_val:.2%}",
                  annotation_position="top left")

    # Format x-axis as percentage
    fig.update_layout(
        title_font=dict(size=24, color="black", family="Calibri", weight="bold"),
        title_x=0.5,
        xaxis=dict(
            showline=True,  # Show outer axis line (border)
            linewidth=1,  # Reduced border thickness for the x-axis
            linecolor='gray',  # Outer line color for the x-axis
            tickformat=".0%", 
            range=[-df["YTDReturn"].max()-0.05, df["YTDReturn"].max()+0.05]
            ),
        # yaxis=dict(
        #     showline=True,  # Show outer axis line (border)
        #     linewidth=1,  # Reduced border thickness for the y-axis
        #     linecolor='gray',  # Outer line color for the y-axis
        #     ),
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor="rgba(0,0,0,0)",   # Transparent plot area
        paper_bgcolor="rgba(0,0,0,0)"  # Transparent overall figure background
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
        title="Companies by Intraday Contribution",
        title_font=dict(size=24, color="black", family="Calibri", weight="bold"),
        title_x=0.5,
        xaxis_title="IntradayContribution",
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
        margin=dict(l=150, r=50, t=50, b=50),
        plot_bgcolor="white",
        showlegend=False
    )

    return fig.to_html(full_html=False)