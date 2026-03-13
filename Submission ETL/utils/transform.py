import pandas as pd
import re

def transform_data(extracted_data):
    print("Mulai membersihkan data...")
    try:
        if not extracted_data:
            return None
            
        df = pd.DataFrame(extracted_data)
        
        df.dropna(subset=['Title', 'Price', 'Rating'], inplace=True)
        
        df = df[df['Title'] != 'Unknown Product']
        df = df[df['Price'] != 'Price Unavailable']
        df = df[df['Rating'] != 'Invalid Rating / 5']
        
        df['Price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
        df['Price'] = df['Price'] * 16000.0
        
        def clean_rating(val):
            val_str = str(val)
            if 'Not Rated' in val_str:
                return 0.0
            match = re.search(r"(\d+\.\d+|\d+)", val_str)
            return float(match.group(1)) if match else 0.0
            
        df['Rating'] = df['Rating'].apply(clean_rating)
        
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').fillna(0).astype('int64')
        df['Size'] = df['Size'].str.replace('Size:', '', regex=False).str.strip()
        df['Gender'] = df['Gender'].str.replace('Gender:', '', regex=False).str.strip()
        
        df.drop_duplicates(subset=['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender'], inplace=True)
        
        df.reset_index(drop=True, inplace=True)
        print(f"Data bersih yang tersisa: {len(df)} baris.")
        return df
        
    except Exception as e:
        print(f"[ERROR] Transformasi gagal: {e}")
        return None
