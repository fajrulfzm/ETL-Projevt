import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_postgres, load_to_gsheets

def get_dummy_df():
    return pd.DataFrame({"Title": ["A"], "Price": [1000]})

def test_load_to_csv(tmp_path):
    df = get_dummy_df()
    file_path = tmp_path / "products.csv"
    result = load_to_csv(df, str(file_path))
    assert result is True

@patch('utils.load.create_engine')
def test_load_to_postgres(mock_engine):
    df = get_dummy_df()
    result = load_to_postgres(df, "user", "pass", "host", "5432", "db")
    assert result is True

@patch('utils.load.Credentials.from_service_account_file')
@patch('utils.load.gspread.authorize')
def test_load_to_gsheets(mock_authorize, mock_creds):
    df = get_dummy_df()
    mock_client = MagicMock()
    mock_authorize.return_value = mock_client
    
    result = load_to_gsheets(df, "dummy.json", "dummy_id")
    assert result is True