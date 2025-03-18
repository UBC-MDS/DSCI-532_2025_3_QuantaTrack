"""
Tests for the `render_scatter_plot` function in `src/components.py`.
"""

import pytest
from src.components import render_scatter_plot

def test_scatter_plot_all():
    """
    Test that providing ['All'] returns a valid HTML string 
    for the entire dataset's scatter plot.
    """
    output = render_scatter_plot(["All"])
    assert isinstance(output, str)
    # Plotly-generated HTML often has <svg> or <div class="plotly"
    assert "<svg" in output.lower() or "plotly" in output.lower()

def test_scatter_plot_empty():
    """
    Test that an empty list also defaults to ['All'].
    """
    output = render_scatter_plot([])
    assert "div" in output.lower()

def test_scatter_plot_single_sector():
    """
    Test specifying one sector to ensure the function 
    properly filters data and still returns HTML.
    """
    output = render_scatter_plot(["Consumer Staples"])
    assert isinstance(output, str)
    assert "<svg" in output.lower()

@pytest.mark.parametrize("sector", ["Energy", "Financials"])
def test_scatter_plot_sector_variants(sector):
    """
    Test multiple single-sector variations to ensure each 
    returns a valid scatter plot.
    """
    output = render_scatter_plot([sector])
    assert "<svg" in output.lower()
