"""
Tests for the `render_ytd_distribution` function in `src/components.py`.
"""

import pytest
from src.components import render_ytd_distribution

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
