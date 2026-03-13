import pandas as pd
from sqlalchemy import create_engine
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse

def load_to_csv(df, file_name="products.csv"):
    """
    Menyimpan DataFrame ke dalam file CSV lokal.
    """
    print(f"Sedang menyimpan data ke {file_name}...")
    try:
        if df is not None and not df.empty:
            df.to_csv(file_name, index=False)
            print(f"[SUCCESS] Data berhasil disimpan ke CSV: {file_name}")
            return True
        else:
            print("[WARNING] Data kosong, gagal menyimpan ke CSV.")
            return False
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke CSV: {e}")
        return False

def load_to_postgres(df, db_user, db_pass, db_host, db_port, db_name, table_name="fashion_products"):
    """
    Menyimpan DataFrame ke database PostgreSQL.
    Menggunakan quote_plus untuk menangani password dengan karakter khusus.
    """
    print(f"Sedang mengirim data ke PostgreSQL (Tabel: {table_name})...")
    try:
        if df is not None and not df.empty:
            safe_password = urllib.parse.quote_plus(db_pass)
            
            conn_url = f'postgresql://{db_user}:{safe_password}@{db_host}:{db_port}/{db_name}'
            engine = create_engine(conn_url)
            
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"[SUCCESS] Data berhasil disimpan ke database PostgreSQL!")
            return True
        else:
            print("[WARNING] Data kosong, gagal menyimpan ke PostgreSQL.")
            return False
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke PostgreSQL: {e}")
        return False

def load_to_gsheets(df, credentials_file, spreadsheet_id, sheet_name="Sheet1"):
    """
    Menyimpan DataFrame ke Google Sheets menggunakan Service Account.
    """
    print(f"Sedang mengunggah data ke Google Sheets...")
    try:
        if df is not None and not df.empty:
            # Setup Scopes dan Kredensial
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
            client = gspread.authorize(creds)
            
            sheet = client.open_by_key(spreadsheet_id)
            worksheet = sheet.worksheet(sheet_name)
            
            worksheet.clear()
            data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
           
            worksheet.update(values=data_to_upload, range_name='A1')
            
            print(f"[SUCCESS] Data berhasil disimpan ke Google Sheets!")
            return True
        else:
            print("[WARNING] Data kosong, gagal menyimpan ke Google Sheets.")
            return False
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke Google Sheets: {e}")
        return False