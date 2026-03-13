import pandas as pd
from utils.transform import transform_data

def test_transform_data_logic():
    raw_data = [
        {
            "Title": "Hoodie Keren", 
            "Price": "$10.00", 
            "Rating": "Rating: ⭐ 4.0 / 5", 
            "Colors": "2 Colors", 
            "Size": "Size: L", 
            "Gender": "Gender: Men"
        },
        {
            "Title": "Unknown Product", # Harus terbuang
            "Price": "Price Unavailable", # Harus terbuang
            "Rating": "Not Rated", 
            "Colors": "0", 
            "Size": "M", 
            "Gender": "Unisex"
        }
    ]
    
    df_clean = transform_data(raw_data)
    
    # Assertions
    assert len(df_clean) == 1 
    assert df_clean.iloc[0]['Price'] == 160000.0 # 10 * 16000
    assert df_clean.iloc[0]['Rating'] == 4.0
    assert df_clean.iloc[0]['Title'] == "Hoodie Keren"

def test_transform_empty_data():
    assert transform_data([]) is None
    assert transform_data(None) is None