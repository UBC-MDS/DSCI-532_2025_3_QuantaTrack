# QuantaTrack Proposal

## 1. Motivation and purpose

The rapidly changing landscape of financial markets demands tools that provide real-time insights and empower investors to make informed decisions with confidence. QuantaTrack was developed to address this need, offering a comprehensive and user-friendly dashboard tailored for monitoring the NASDAQ100. With a focus on accessibility and functionality, the platform aims to equip investors with the necessary tools to track critical performance metrics, analyze trends, and assess market shifts—all in one place.

At its core, QuantaTrack seeks to simplify the complex world of investing by consolidating essential data into an intuitive interface. The app's advanced analytics tools enable users to closely monitor individual stocks, spot emerging trends, and identify potential investment opportunities. By delivering detailed performance analysis, QuantaTrack helps investors not only to track their portfolio but also to anticipate market movements and adapt their strategies accordingly.

The purpose of QuantaTrack is to bridge the gap between technical complexity and practical usability. We want to ensure that investors, whether seasoned or new to the market, can quickly access the information they need to make decisions that align with their investment goals. In an era where time is critical, QuantaTrack aims to be the go-to platform for navigating the NASDAQ100, offering reliable data and insights that support effective decision-making in a fast-paced market environment.

## 2. Description of the data

The dataset used for this project is derived from the NASDAQ 100 Companies and includes key financial metrics for each company in the index. 

It contains several variables crucial for analyzing the stock performance of the companies listed, 

- Basic Information (`Ticker`, `Name`, `Sector`)

- Stock Performance and Price (`Price`, `IntradayReturn`, `YTDReturn`, `IntradayContribution`, `YTDContribution`)

- Valuation Metrics (`PE`, `PB`, `Dividend Yield`, `Dividend`, `Profit_TTM`)

- Market Data (`Volume`, `Amount` ,`MarketCap`, `SharesOutstanding`, `Weight`)

- Time (`Date`)

We plan to visualize market trends and compare sector-wise contributions to the overall performance. 

Additionally, we will derive new variables such as (`market_trend_patterns`) and (`correlation_between_sector_performance`) and (`overall_returns`) to understand the broader market shifts.

This analysis will assist in identifying patterns and understanding market dynamics, particularly focusing on sector performance and individual stock behavior within the NASDAQ 100 index.

## 3. Research questions

John is an investment analyst at a hedge fund, tasked with evaluating the performance of large-cap stocks, particularly those in major indices such as the NASDAQ 100. He logs into the QuantaTrack app, which provides an interactive dashboard for visualizing the performance of companies within the NASDAQ 100 index. John’s goal is to explore the performance metrics of various companies in the index, understand their contribution to market movements, and identify key stocks that may drive future market trends.

As John navigates the dashboard, he starts by filtering the data to focus on the Information Technology sector, which has a significant representation in the NASDAQ 100. He examines key metrics such as market cap, PE ratio, intraday return, and YTD return. By sorting the data, John quickly identifies that Apple Inc and Microsoft Corp dominate the index in terms of market cap and weight. These two companies have a major influence on the overall market movement, and their stock price fluctuations are highly correlated with the performance of the NASDAQ 100.

Next, John dives deeper into the intraday return metric and notices that Tesla Inc is seeing strong performance for the day, with a high intraday return compared to other stocks. This prompts him to investigate further, and he speculates that Tesla’s stock is likely reacting to a positive news cycle or a market event. By analyzing these metrics and comparing them across companies, John concludes that Apple and Microsoft will continue to drive the index’s performance, while Tesla may offer shorter-term opportunities for growth. Based on these insights, John recommends an increased allocation of the fund’s capital into Apple and Microsoft, while keeping an eye on Tesla for potential adjustments.

## 4. App sketch and description
# QuantaTrack Proposal

## 1. Motivation and purpose

The rapidly changing landscape of financial markets demands tools that provide real-time insights and empower investors to make informed decisions with confidence. QuantaTrack was developed to address this need, offering a comprehensive and user-friendly dashboard tailored for monitoring the NASDAQ100. With a focus on accessibility and functionality, the platform aims to equip investors with the necessary tools to track critical performance metrics, analyze trends, and assess market shifts—all in one place.

At its core, QuantaTrack seeks to simplify the complex world of investing by consolidating essential data into an intuitive interface. The app's advanced analytics tools enable users to closely monitor individual stocks, spot emerging trends, and identify potential investment opportunities. By delivering detailed performance analysis, QuantaTrack helps investors not only to track their portfolio but also to anticipate market movements and adapt their strategies accordingly.

The purpose of QuantaTrack is to bridge the gap between technical complexity and practical usability. We want to ensure that investors, whether seasoned or new to the market, can quickly access the information they need to make decisions that align with their investment goals. In an era where time is critical, QuantaTrack aims to be the go-to platform for navigating the NASDAQ100, offering reliable data and insights that support effective decision-making in a fast-paced market environment.

## 2. Description of the data

The dataset used for this project is derived from the NASDAQ 100 Companies and includes key financial metrics for each company in the index. 

It contains several variables crucial for analyzing the stock performance of the companies listed, 

- Basic Information (`Ticker`, `Name`, `Sector`)

- Stock Performance and Price (`Price`, `IntradayReturn`, `YTDReturn`, `IntradayContribution`, `YTDContribution`)

- Valuation Metrics (`PE`, `PB`, `Dividend Yield`, `Dividend`, `Profit_TTM`)

- Market Data (`Volume`, `Amount` ,`MarketCap`, `SharesOutstanding`, `Weight`)

- Time (`Date`)

We plan to visualize market trends and compare sector-wise contributions to the overall performance. 

Additionally, we will derive new variables such as (`market_trend_patterns`) and (`correlation_between_sector_performance`) and (`overall_returns`) to understand the broader market shifts.

This analysis will assist in identifying patterns and understanding market dynamics, particularly focusing on sector performance and individual stock behavior within the NASDAQ 100 index.

## 3. Research questions

John is an investment analyst at a hedge fund, tasked with evaluating the performance of large-cap stocks, particularly those in major indices such as the NASDAQ 100. He logs into the QuantaTrack app, which provides an interactive dashboard for visualizing the performance of companies within the NASDAQ 100 index. John’s goal is to explore the performance metrics of various companies in the index, understand their contribution to market movements, and identify key stocks that may drive future market trends.

As John navigates the dashboard, he starts by filtering the data to focus on the Information Technology sector, which has a significant representation in the NASDAQ 100. He examines key metrics such as market cap, PE ratio, intraday return, and YTD return. By sorting the data, John quickly identifies that Apple Inc and Microsoft Corp dominate the index in terms of market cap and weight. These two companies have a major influence on the overall market movement, and their stock price fluctuations are highly correlated with the performance of the NASDAQ 100.

Next, John dives deeper into the intraday return metric and notices that Tesla Inc is seeing strong performance for the day, with a high intraday return compared to other stocks. This prompts him to investigate further, and he speculates that Tesla’s stock is likely reacting to a positive news cycle or a market event. By analyzing these metrics and comparing them across companies, John concludes that Apple and Microsoft will continue to drive the index’s performance, while Tesla may offer shorter-term opportunities for growth. Based on these insights, John recommends an increased allocation of the fund’s capital into Apple and Microsoft, while keeping an eye on Tesla for potential adjustments.

## 4. App sketch and description

### App Sketch

![QuantaTrack Dashboard Sketch](../img/sketch.png)

### High-Level Description

The QuantaTrack dashboard consists of multiple interactive components designed for real-time market monitoring. Users can filter data, analyze key financial metrics, and visualize trends efficiently. The main components of the dashboard include:

- **Filters & Controls Panel (Left Sidebar):** Users can filter companies based on sector, market capitalization, and time range. A search box allows quick lookup of specific companies.
- **NASDAQ 100 Industry Distribution (Pie Chart):** Displays sector-wise distribution of companies within the NASDAQ 100 index.
- **Top/Bottom 10 Intraday Contributors (Bar Charts - Horizontal & Vertical):** Highlights the top-performing and worst-performing companies based on their intraday returns.
- **Sector-Wise Weighted Return (Bubble/Scatter Plot):** Helps investors compare sector performance with respective market weights.
- **YTD Return Distribution (Histogram):** Shows the spread of returns across all companies in the NASDAQ 100, helping users analyze market trends.
- **Model Price vs. Actual Price (Scatter Plot):** Compares real stock prices to predicted model values, with dividend yield represented through color intensity.
- **Stock Screener Table:** A sortable and searchable table providing key stock-level financial metrics.

Users will interact with the dashboard by adjusting filters, selecting specific stocks, and analyzing detailed company performance to make informed investment decisions.

