import pytest
import warnings
import json
import pandas as pd
from io import StringIO

from dash import Dash
from dash._callback_context import context_value
from dash._utils import AttributeDict
from unittest.mock import patch, MagicMock

from src.callbacks import *

for warning in [DeprecationWarning, UserWarning, FutureWarning]:
    warnings.simplefilter("ignore", warning)

# Run test in terminal with pytest tests/test_callbacks.py
@pytest.fixture
def app():
    """Create a Dash app with registered callbacks"""
    app = Dash(__name__)
    register_callbacks(app)
    return app

# @pytest.fixture
# def test_data():
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

@pytest.fixture
def test_data():
    """Sample test data for callbacks that matches QQQM holdings format"""
    return [
        {
            "Ticker": "AAPL",
            "Name": "Apple Inc.",
            "Weight": 12.85,
            "Price": 150.23,
            "IntradayReturn": 0.015,
            "Volume": 55000000,
            "Amount": 8265000000,
            "IntradayContribution": 0.00193,
            "MarketCap": 2500000000000,
            "YTDReturn": 0.15,
            "YTDContribution": 0.0193,
            "PE": 25.0,
            "PB": 35.8,
            "Profit_TTM": 100000000000,
            "DividendYield": 0.006,
            "Dividend": 0.96,
            "SharesOutstanding": 15000000000,
            "Sector": "Information Technology",
            "Date": "2025-03-12"
        },
        {
            "Ticker": "MSFT",
            "Name": "Microsoft Corporation",
            "Weight": 10.25,
            "Price": 420.45,
            "IntradayReturn": 0.008,
            "Volume": 25000000,
            "Amount": 10511250000,
            "IntradayContribution": 0.00082,
            "MarketCap": 3100000000000,
            "YTDReturn": 0.12,
            "YTDContribution": 0.0123,
            "PE": 30.0,
            "PB": 15.2,
            "Profit_TTM": 103000000000,
            "DividendYield": 0.008,
            "Dividend": 3.36,
            "SharesOutstanding": 7500000000,
            "Sector": "Information Technology",
            "Date": "2025-03-12"
        }
    ]

def test_update_interval_speed_callback(app):
    """Test the update interval speed callback"""
    # Get the callback function using the correct ID from callback_map
    
    callback_id = "..data-update-interval.disabled...data-update-interval.interval.."
    callback_function = app.callback_map[callback_id]["callback"]

    outputs_list = [
    {"id": "data-update-interval", "property": "disabled"},
    {"id": "data-update-interval", "property": "interval"}
    ]
    
    ctx = AttributeDict({
        "triggered_inputs": [{"prop_id": "update-speed.value", "value": "3s"}],
        "inputs_list": [{"id": "update-speed", "property": "value"}],
        "outputs_list": outputs_list,
        "inputs": {"update-speed.value": "3s"},
        "states": {},
        "outputs": {},
        "callback_context": True
    })
    context_value.set(ctx)

    result = callback_function("3s", outputs_list=outputs_list)
    
    # Parse the JSON-like string result
    assert isinstance(result, str)
    assert '"disabled":false' in result
    assert '"interval":3000' in result
    
    # Test No update case
    result_no_update = callback_function("No update", outputs_list=outputs_list)
    assert isinstance(result_no_update, str)
    assert '"disabled":true' in result_no_update
    assert '"interval":1000' in result_no_update


def test_update_table_callback(app, test_data):
    """Test the table update callback"""
    callback_function = app.callback_map["stock-table.rowData"]["callback"]
    
    outputs_list = [{"id": "stock-table", "property": "rowData"}]
    ctx = AttributeDict({
        "triggered_inputs": [{"prop_id": "filter-ticker.value", "value": "AAPL"}],
        "inputs_list": [
            {"id": "filter-ticker", "property": "value"},
            {"id": "filter-name", "property": "value"},
            {"id": "filter-sector", "property": "value"},
            {"id": "data-store", "property": "data"}
        ],
        "outputs_list": outputs_list,
        "inputs": {
            "filter-ticker.value": "AAPL",
            "filter-name.value": "",
            "filter-sector.value": ["Information Technology"],  # Match the actual sector name
            "data-store.data": test_data
        },
        "states": {},
        "outputs": {},
        "callback_context": True
    })
    context_value.set(ctx)

    # Call callback without outputs_list parameter
    result = callback_function("AAPL", "", ["Information Technology"], test_data, outputs_list=outputs_list)
    
    # Parse JSON string result
    result_dict = json.loads(result)
    assert isinstance(result_dict, dict)
    assert "multi" in result_dict
    assert "response" in result_dict
    
    # Get the filtered data from response
    table_data = result_dict["response"]["stock-table"]["rowData"]
    assert isinstance(table_data, dict)
    assert table_data["Ticker"] == "AAPL"
    assert table_data["Sector"] == "Information Technology"

def test_download_csv_callback(app, test_data):
    """Test the CSV download callback"""

    callback_function = app.callback_map["download-csv.data"]["callback"]
    outputs_list = [{"id": "download-csv", "property": "data"}]

    # Create minimal context
    ctx = AttributeDict({
        "triggered_inputs": [{"prop_id": "download-csv-btn.n_clicks", "value": 1}],
        "inputs_list": [{"id": "download-csv-btn", "property": "n_clicks"}],
        "outputs_list": outputs_list,
        "inputs": {"download-csv-btn.n_clicks": 1},
        "states": {},
        "outputs": {},
        "callback_context": True,
        "triggered": [{"prop_id": "download-csv-btn.n_clicks", "value": 1}]  # Add triggered here
    })

    # Set up callback context
    context_value.set(ctx)

    # Create a mock callback context
    mock_ctx = MagicMock()
    mock_ctx.triggered = [{"prop_id": "download-csv-btn.n_clicks", "value": 1}]

    # Mock both callback context and dcc.send_string
    with patch('dash.callback_context', mock_ctx):
        with patch('dash.dcc.send_string', side_effect=lambda content, filename: [{
            'content': content,
            'filename': filename,
            'type': None,
            'base64': False
        }]) as mock_send_string:
            # Call the callback
            result = callback_function(1, test_data, ["Information Technology"], outputs_list=outputs_list)
            
            # Verify response structure
            result_dict = json.loads(result)
            assert isinstance(result_dict, dict)
            assert "multi" in result_dict
            assert "response" in result_dict
            
            # Verify download data
            download_data = result_dict["response"]["download-csv"]["data"]
            assert isinstance(download_data, dict)
            assert "content" in download_data
            assert "filename" in download_data
            assert download_data["filename"] == "QuantaTrack_Output.csv"
            
            # Verify CSV content
            df = pd.read_csv(StringIO(download_data["content"]))
            assert len(df) > 0
            assert "AAPL" in df["Ticker"].values
            assert "MSFT" in df["Ticker"].values

if __name__ == "__main__":
    pytest.main(["-v"])