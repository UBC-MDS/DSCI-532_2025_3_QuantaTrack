import pytest
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

# To run the tests:
if __name__ == "__main__":
    pytest.main()