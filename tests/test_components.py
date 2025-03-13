import pytest
from unittest.mock import patch
from bs4 import BeautifulSoup
import pandas as pd
from src.components import *

# # Sample data to mock getQQQMHolding function
# @pytest.fixture
# def sample_data():
#     return pd.DataFrame({
#         'Ticker': ['AAPL', 'MSFT', 'GOOGL'],
#         'Name': ['Apple', 'Microsoft', 'Google'],
#         'Weight': [0.05, 0.07, 0.06],
#         'Price': [150, 200, 2500],
#         'IntradayReturn': [0.002, 0.003, 0.001],
#         'Volume': [100000, 150000, 200000],
#         'Amount': [10000000, 30000000, 50000000],
#         'IntradayContribution': [0.0001, 0.0002, 0.00015],
#         'MarketCap': [2500000000, 1800000000, 1500000000],
#         'YTDReturn': [0.15, 0.1, 0.12],
#         'YTDContribution': [0.01, 0.02, 0.015],
#         'PE': [30, 35, 40],
#         'PB': [8, 6, 7],
#         'Profit_TTM': [5000000, 7000000, 4000000],
#         'DividendYield': [0.006, 0.005, 0.004],
#         'Dividend': [0.5, 1.5, 0.3],
#         'SharesOutstanding': [5000000, 10000000, 12000000],
#         'Sector': ['Tech', 'Tech', 'Finance'],
#         'Date': ['2025-03-01', '2025-03-01', '2025-03-01']
#     })

# Test case for render_scatter_plot 
def test_render_scatter_plot_all_sectors():
    """Test when no sectors are selected (defaults to 'All')."""
    selected_sectors = ["All"]
    result = render_scatter_plot(selected_sectors)
    assert isinstance(result, str)  # Ensure the output is an HTML string
    print("Test 1 (All sectors): Passed")

def test_render_scatter_plot_empty_sectors():
    """Test when an empty list is provided (defaults to 'All')."""
    selected_sectors = []
    result = render_scatter_plot(selected_sectors)
    assert isinstance(result, str)  # Ensure the output is an HTML string
    print("Test 2 (Empty list): Passed")

def test_render_scatter_plot_specific_sectors():
    """Test when specific sectors are selected."""
    selected_sectors = ["Information Technology", "Consumer Staples"]
    result = render_scatter_plot(selected_sectors)
    assert isinstance(result, str)  # Ensure the output is an HTML string
    print("Test 3 (Specific sectors): Passed")

# To run the tests:
if __name__ == "__main__":
    pytest.main()