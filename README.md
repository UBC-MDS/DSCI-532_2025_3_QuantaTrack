# QuantaTrack

This project is about making a dynamic dashboard of NASDAQ100 tracking.

## 📖 The Problem

Investors often struggle with navigating complex and overwhelming market data to identify key trends and make informed investment decisions. 
With an abundance of financial information, tracking performance metrics and staying updated with real-time insights becomes challenging, 
especially when dealing with fast-evolving markets like the NASDAQ 100. 
Many investors are left with fragmented data, making it difficult to draw actionable conclusions and plan effective investment strategies.

## 💡 The Solution

QuantaTrack addresses these challenges by providing a comprehensive, real-time dashboard designed to monitor the NASDAQ 100. 
By consolidating essential performance metrics and visualizing trends, 
it empowers investors to quickly assess market movements and individual stock performance. 
With an intuitive interface and advanced analytics tools, QuantaTrack offers a streamlined platform that helps users stay informed 
and make confident, data-driven investment decisions in a dynamic market environment.

## 💻 Usage

### Overview

The QuantaTrack dashboard is organized into a sidebar for user input and a data display section. 

In the sidebar, users can filter data by sector, allowing for a customized view of the data. 
The data display section offers real-time insights on key performance metrics, 
including intraday performance, sector composition, and stock metrics like dividend yield and PE ratio. 

Below the charts, users can also select their preferred refresh interval for the stock screener table, 
with updates available every 3 or 10 seconds. 
The search box allows users to find specific tickers or company names in the table, 
and they can download the data in CSV format based on the current view for further analysis.

### Demo

[DEMO TO BE ADDED]

### Dashboard

Visit QuantaTrack [ATTACH ON RENDER LINK] for our dashboard directly!

### Developer Guide

1.  Clone the repository

``` bash
git clone git@github.com:UBC-MDS/DSCI-532_2025_3_QuantaTrack.git
```

2.  Create the virtual environment

``` bash
conda env create -f environment.yml
conda activate quantatrack
```

3.  Render the dashboard

``` bash
make run
```

## 👥 Contributors

Ethan Fang ([\@ethanfang08](https://github.com/ethanfang08)), Jenny Zhang ([\@JennyonOort](https://github.com/JennyonOort)), Kevin Gao ([\@kegao1995](https://github.com/kegao1995)), Ziyuan Zhao ([\@cherylziunzhao](https://github.com/cherylziunzhao))

## 🖇 Contributing

Interested in contributing? Check out the [contributing guidelines](./CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](./CODE_OF_CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## 📚 License

The QuantaTrack dashboard is licensed under the terms of the [MIT license and Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](./LICENSE.md).

## 🤜 Support

If you encounter any issues, require assistance, need to report a bug or request a feature, please file an issue through our [GitHub Issues](https://github.com/UBC-MDS/DSCI-532_2025_3_QuantaTrack/issues).