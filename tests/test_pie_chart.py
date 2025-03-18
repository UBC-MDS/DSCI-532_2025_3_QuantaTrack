"""
Tests for the `render_pie_chart` function in `src/components.py`.
"""

import pytest
from src.components import render_pie_chart

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
