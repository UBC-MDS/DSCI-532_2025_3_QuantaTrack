## Parts Implemented So Far
We have established the backbone of the QuantaTrack dashboard, providing users with key financial insights on the NASDAQ 100. 
Key visualizations include a pie chart that shows the sector composition of the index, 
a horizontal bar chart highlighting intraday performance, a scatter plot that compares dividend yield with PE ratio, 
and a histogram that displays year-to-date returns.  

The dashboard is fully interactive, with the sector filter controlling all charts. 
This ensures that when users select a sector, all visualizations and the table update accordingly, offering a cohesive view of market data. 
Additionally, a stock screener table presents key financial data for NASDAQ 100 companies (e.g., market cap, weight, YTD return, etc.) 
and allows users to filter results by ticker or company name.

## Parts Done Differently
We addressed several challenges to improve usability. One key improvement was ensuring that the dropdown filters for sectors 
and tickers work seamlessly together, preventing errors when incompatible filters are applied. 
Additionally, we implemented real-time data refresh, updating the dashboard every 3 to 10 seconds to provide the latest market data.  

To enhance clarity, we repositioned the search bar above the table, ensuring users understand that it only applies to the table filters 
and not the charts. We also added a download CSV button, enabling users to export data based on the current filter state.

## Intentional Deviations from Visualization Practices
While industry best practices recommend using no more than five colors in a chart, 
we are required to use 10+ colors in order to represent the various sectors in the NASDAQ 100. 
Given the diversity of sectors in the index, this choice ensures each sector is clearly distinguishable, 
improving clarity and making comparisons easier for users.

## Features Still in Development
Several exciting features are still under development. 
We are working on adding real-time price, intraday price and volume movements cards at the top, 
providing users immediate access to crucial market data. 
In addition, We are in the process of updating the pie chart to show the top companies' weight when not all sectors are selected, 
providing a more informative perspective on company dominance. 
The search box will soon support multiple tickers or company names, enhancing its flexibility. 
The CSV download feature will be enhanced to capture the sort state as well. 
Finally, we would like to set up infrastructure for continuous deployment, 
which will allow QuantaTrack to expand with additional financial datasets, 
enabling users to track more indices and sectors beyond the NASDAQ 100.

## Limitations and Potential Future Improvements

While QuantaTrack is a real-time dashboard, one potential improvement is the ability to store historical data for time-series comparisons. 
This would provide valuable insights but could introduce challenges in terms of computation and storage, 
potentially affecting performance with large datasets. 
To mitigate this, we plan to implement data aggregation techniques to streamline the dataset without losing important insights. 
Additionally, we aim to enhance the customizability of visualizations, allowing users to tailor chart appearance and granularity, 
enabling more personalized and detailed analysis to meet specific needs.
