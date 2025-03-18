import pytest
import pandas as pd
from src.components import getQQQMHolding

def test_getQQQMHolding_returns_data():
    """Test that getQQQMHolding returns a non-empty DataFrame with holding data."""
    holdings = getQQQMHolding()
    assert isinstance(holdings, pd.DataFrame), "Output should be a pandas DataFrame."
    assert not holdings.empty, "Holdings DataFrame should not be empty."
