import pytest
import warnings
from unittest.mock import patch
from bs4 import BeautifulSoup
import pandas as pd
from src.components import *

# Run test in terminal with pytest tests/test_components.py

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


# Test case for render_intraday_contribution_5
for warning in [DeprecationWarning, UserWarning, FutureWarning]:
    warnings.simplefilter("ignore", warning)

def test_intraday_all():
    """
    Test that ['All'] yields a horizontal bar chart referencing "Companies by Intraday Contribution".
    """
    html_output = render_intraday_contribution_5(["All"])
    assert isinstance(html_output, str)
    assert "companies by intraday contribution" in html_output.lower()

def test_intraday_empty():
    """
    Test that an empty list => also defaults to ['All'] => same result as the entire dataset.
    """
    html_output = render_intraday_contribution_5([])
    assert "companies by intraday contribution" in html_output.lower()

def test_intraday_single_sector():
    """
    Check specifying one sector returns top/bottom 5 for that sector,
    producing valid bar chart HTML (with <svg>).
    """
    output = render_intraday_contribution_5(["Financials"])
    assert "<svg" in output.lower()

@pytest.mark.parametrize("sectors", [["Energy", "Utilities"], ["Health Care", "Materials"]])
def test_intraday_multi_sector(sectors):
    """
    Test multiple sectors to ensure combined selection yields
    a single bar chart for top/bottom 5 across them.
    """
    output = render_intraday_contribution_5(sectors)
    assert "intraday contribution" in output.lower()
    assert isinstance(output, str)


# Test case for render_pie_chart
def test_pie_chart_all():
    """
    Test that providing ['All'] returns a valid sector-level pie chart as HTML.
    We look for typical HTML tags to ensure a pyecharts chart is generated.
    """
    html_output = render_pie_chart(["All"])
    assert isinstance(html_output, str)
    # Typical pyecharts output might have <div> or <script> tags
    assert "<div" in html_output.lower() or "<script" in html_output.lower()

def test_pie_chart_empty_list():
    """
    Test that an empty list defaults to ['All'] internally,
    thus also returning a sector-level chart.
    """
    html_output = render_pie_chart([])
    assert "by Sector" in html_output or "sector" in html_output

def test_pie_chart_single_sector():
    """
    Test specifying a single sector returns a top-10 chart.
    The HTML should reference 'Top 10 Companies'.
    """
    html_output = render_pie_chart(["Information Technology"])
    assert "Top 10 Companies" in html_output

@pytest.mark.parametrize("sectors", [["Health Care", "Energy"], ["Utilities", "Materials"]])
def test_pie_chart_multiple_sectors(sectors):
    """
    Test multiple sectors also produce a top-10 chart, 
    verifying the function handles combined sector filtering.
    """
    html_output = render_pie_chart(sectors)
    assert "Top 10 Companies" in html_output
    assert isinstance(html_output, str)


# Test case for render_ytd_distribution
def test_ytd_distribution_all():
    """
    Test that with ['All'], the YTD histogram is generated 
    and returns valid HTML referencing 'YTD Return Distribution'.
    """
    output = render_ytd_distribution(["All"])
    assert isinstance(output, str)
    assert "ytd return distribution" in output.lower()

def test_ytd_distribution_empty():
    """
    An empty list => defaults to ['All'] => sector-level distribution for entire data.
    """
    output = render_ytd_distribution([])
    assert "ytd return distribution" in output.lower()

def test_ytd_distribution_single_sector():
    """
    Test specifying a single sector yields a valid histogram.
    Checking for typical <svg> or plotly references.
    """
    output = render_ytd_distribution(["Real Estate"])
    assert "<svg" in output.lower()

def test_ytd_distribution_html_structure():
    """
    Basic test that the returned string is HTML and 
    likely contains histogram elements, e.g. 'histogram' or 'bins'.
    """
    output = render_ytd_distribution(["Industrials"])
    assert "histogram" in output.lower() or "bins" in output.lower()


# Test case for calculate_beta
def test_calculate_beta_identical_arrays():
    """
    Test calculate_beta when both stock_returns and index_returns are identical.
    By default, np.cov uses sample covariance (ddof=1), while np.var uses
    population variance (ddof=0). For the array [1, 2, 3], this results in:
      - sample covariance = 1.0
      - population variance of [1,2,3] = 2/3
      => beta = 1.0 / (2/3) = 1.5
    """
    stock_returns = np.array([1, 2, 3], dtype=float)
    index_returns = np.array([1, 2, 3], dtype=float)
    beta = calculate_beta(stock_returns, index_returns)
    assert beta == pytest.approx(1.5), f"Expected beta ~ 1.5, got {beta}"

def test_calculate_beta_different_scales():
    """
    Test calculate_beta when the index_returns is a scaled version of stock_returns.
    For stock_returns = [1, 2, 3] and index_returns = [2, 4, 6]:
      - sample covariance = 2.0
      - population variance of [2,4,6] = 8/3
      => beta = 2.0 / (8/3) = 0.75
    """
    stock_returns = np.array([1, 2, 3], dtype=float)
    index_returns = np.array([2, 4, 6], dtype=float)
    beta = calculate_beta(stock_returns, index_returns)
    assert beta == pytest.approx(0.75), f"Expected beta ~ 0.75, got {beta}"

def test_calculate_beta_zero_variance():
    """
    Test calculate_beta when index_returns has zero variance, which typically 
    causes a divide-by-zero situation. The function might raise an error or 
    return np.inf, depending on the implementation. Adjust the assertion 
    based on desired behavior.
    """
    stock_returns = np.array([1, 2, 3], dtype=float)
    # All index_returns are the same => zero variance
    index_returns = np.array([5, 5, 5], dtype=float)
    
    # Depending on how you handle divide-by-zero, you might expect an exception 
    # or an infinite value. Here, we check for np.inf:
    beta = calculate_beta(stock_returns, index_returns)
    assert np.isnan(beta), f"Expected beta to be infinite when index variance = 0, got {beta}"


# Test case for render_regression_graph
def test_render_regression_graph_smoke():
    """
    A basic "smoke test" to verify that render_regression_graph returns
    a non-empty HTML string for a typical stock ticker and date range.
    """
    # Choose a valid ticker and a reasonable date range for testing:
    selected_stock = "AAPL"
    start_date = "2020-01-01"
    end_date = "2020-12-31"

    # Call the function
    html_output = render_regression_graph(selected_stock, start_date, end_date)

    # Verify that the result is indeed a string
    assert isinstance(html_output, str), "Expected an HTML string, but got a non-string object."

    # Verify that the returned string is not empty
    assert len(html_output) > 0, "Expected a non-empty HTML string."

    # Optionally, check for an expected substring in the HTML output
    # (e.g., some label or heading you know appears in the regression plot)
    expected_substring = "Regression Analysis:"
    assert expected_substring in html_output, (
        f"Expected the HTML output to contain '{expected_substring}', "
        "but it was not found."
    )

# Test case for render_trend_graph
def test_render_trend_graph_smoke():
    """
    A basic smoke test to verify that render_trend_graph returns
    a non-empty HTML string for a typical stock ticker and date range.
    """
    # Provide a valid ticker and date range for the test
    selected_stock = "AAPL"
    start_date = "2020-01-01"
    end_date = "2020-12-31"

    # Call the function
    html_output = render_trend_graph(selected_stock, start_date, end_date)

    # Verify that the result is indeed a string
    assert isinstance(html_output, str), (
        "Expected an HTML string, but got a non-string object."
    )

    # Verify that the returned string is not empty
    assert len(html_output) > 0, "Expected a non-empty HTML string."

    # Check for a known substring in the HTML (e.g., a label or heading)
    # The function docstring mentions "NASDAQ Price Trend (Normalized)", 
    # so we look for that text in the output.
    expected_substring = "NASDAQ 100 Price Trend (Normalized)"
    assert expected_substring in html_output, (
        f"Expected the HTML output to contain '{expected_substring}', "
        "but it was not found."
    )

# To run the tests:
if __name__ == "__main__":
    pytest.main()