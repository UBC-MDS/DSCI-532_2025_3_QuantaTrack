## Parts Implemented Since Milestone 2

Since Milestone 2, we've made key updates to the QuantaTrack dashboard, focusing on layout, table display, and functionality. The **dashboard layout** was restructured to fit all content on a single page, improving navigation. Separate tabs for charts and the table were introduced, allowing users to focus on one without information overload.

The **table display** was improved for better usability, with more consistent scales that make it easier to compare key metrics like market cap, YTD return, and weight. This restructuring simplifies dataset navigation and enhances clarity.

Additionally, a new **Beta Analysis tab** was added, offering a space for users to explore stock volatility in relation to the market. This isolates the risk analysis metric, making it more accessible without cluttering the dashboard.

## Parts Done Differently from Sketch

There haven't been major deviations from the original sketch and proposal. However, we've added intentional improvements for usability, such as the **refresh time interval**, **Beta Analysis tab**, separate tabs for charts and tables, and an enhanced table with better filters. These adjustments improve the user experience without straying from the design.

## Features Yet to Implement (Not From Original Proposal/Sketch but Inspirations from Milestone 2)

One potential addition is **real-time QQQM price and volume updates**, to be displayed on the right side of the dashboard. However, due to **spacing constraints** and concerns about overwhelming users, this feature hasn't been implemented. As it's not a core requirement and may not add much value, we might decide to omit it.

We also considered enabling **multiple ticker searches** but found it could complicate text recognition. Instead, we added **filters by range** for each column in the table, allowing users to narrow down search results based on specific criteria like market cap or YTD return, which better suits investment decisions.

### Challenging Section

After discussions with our instructor, Daniel, our challenge was identified as adjusting the **table's dynamic interaction**. Previously, refreshing the table would reset sorting and filtering, causing frustration. We've now implemented a solution that preserves sorting and filtering during data refresh, even when sector and filter selections change. This was challenging, but it now works seamlessly.

## Intentional Deviations from Visualization Practices

Same as Milestone 2 Reflection.

## Limitations and Potential Future Improvements

While the dashboard has evolved, there are still areas for improvement. The current **real-time data refresh** can cause lag, particularly with multiple filters. Future plans include optimizing this mechanism to reduce delays.

Looking ahead, expanding the dashboard **beyond the NASDAQ 100** could attract a broader audience. A **continuous deployment pipeline** would make it easier to integrate new datasets and indices, allowing users to track additional sectors or stocks as the platform grows.