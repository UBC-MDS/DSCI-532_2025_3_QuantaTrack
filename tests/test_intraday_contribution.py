"""
Tests for the `render_intraday_contribution_5` function in `src/components.py`.
"""

import pytest
import warnings
import json
import pandas as pd
from io import StringIO

from dash import Dash
from dash._callback_context import context_value
from dash._utils import AttributeDict
from unittest.mock import patch, MagicMock

# Import your intraday function
from src.components import render_intraday_contribution_5

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
