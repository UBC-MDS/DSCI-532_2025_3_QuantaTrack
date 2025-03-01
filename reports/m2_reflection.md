## Parts Implemented So Far

We have established the backbone of the QuantaTrack dashboard, providing users with key financial insights on the NASDAQ 100.  
Key visualizations include a pie chart that shows the sector composition of the index, a horizontal bar chart highlighting intraday performance, a scatter plot that compares dividend yield with the PE ratio, and a histogram that displays year-to-date returns.

The dashboard is fully interactive, with the sector filter controlling all charts. This ensures that when users select a sector, all visualizations and the table update accordingly, offering a cohesive view of market data. Additionally, a stock screener table presents key financial data for NASDAQ 100 companies (e.g., market cap, weight, YTD return, etc.) to allow users to carry out downstream analysis by filtering results using ticker or name search and by sorting each feature in ascending or descending order.

## Parts Done Differently

We addressed several challenges to improve usability. One key improvement was ensuring that the dropdown filters for sectors and tickers work seamlessly together, preventing errors when incompatible filters are applied. Additionally, we implemented real-time data refresh, updating the dashboard every 3 or 10 seconds to provide the latest market data.

To enhance clarity, we repositioned the search bar above the table, ensuring users understand that it only applies to the table filters and not the charts. We also added a download CSV button, enabling users to export data based on the current filter state.

## Intentional Deviations from Visualization Practices

While industry best practices recommend using no more than five colors in a chart, we are required to use more than ten colors in order to represent the various sectors in the NASDAQ 100. Given the diversity of sectors in the index, this choice ensures each sector is clearly distinguishable, improving clarity and making comparisons easier for users.

## Features Still in Development

Several exciting features are currently in development. We're working on adding real-time QQQ price updates and intraday volume movement cards at the top, giving users immediate access to essential market data. The search box will soon support multiple tickers or company names, offering greater flexibility. Another potential feature under consideration is the ability to store historical data for time-series comparisons, such as beta analysis. Lastly, we aim to establish infrastructure for continuous deployment, which will allow QuantaTrack to expand with additional financial datasets, enabling users to track more indices and sectors beyond the NASDAQ 100.

## Limitations and Potential Future Improvements

The abundance of information on the dashboard can lead to excessive scrolling, and the current layout could better utilize the available space. Additionally, the dashboard is currently a bit slow, possibly due to the combined effects of refreshing real-time data and filtering.

To address these issues, we plan to implement more efficient data aggregation techniques and optimize the update process, ensuring faster data refresh without compromising the quality of insights. We also aim to improve the layout for better usability and enhance the customizability of visualizations, allowing users to adjust chart appearance and granularity for a more personalized experience.
