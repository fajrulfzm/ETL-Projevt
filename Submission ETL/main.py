from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_postgres, load_to_gsheets

def run_etl():
    print("=== Memulai ETL Pipeline ===")
    
    # 1. EXTRACT
    print("\n[1] TAHAP EKSTRAKSI")
    raw_data = extract_data(total_pages=50) 
    
    if raw_data:
        # 2. TRANSFORM
        print("\n[2] TAHAP TRANSFORMASI")
        clean_df = transform_data(raw_data)
        
        if clean_df is not None:
            # 3. LOAD
            print("\n[3] TAHAP LOAD (Ke 3 Repositori)")
            
            # a. Simpan ke CSV
            load_to_csv(clean_df, "products.csv")
            
            # b. Simpan ke PostgreSQL
            DB_USER = 'postgres'
            DB_PASS = ";';';';'"
            DB_HOST = 'localhost'
            DB_PORT = '5432'
            DB_NAME = 'fashion_db'
            load_to_postgres(clean_df, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
            
            # c. Simpan ke Google Sheets
            CREDENTIALS_FILE = 'google-sheets-api.json'
            SPREADSHEET_ID = '19yZxEqLe36OmyfpFvqIc1aWffsnycS4MHqkB604And' 
            load_to_gsheets(clean_df, CREDENTIALS_FILE, SPREADSHEET_ID)
            
            print("\n=== ETL Pipeline Selesai ===")
        else:
            print("Proses ETL berhenti karena kegagalan pada tahap Transformasi.")
    else:
        print("Proses ETL berhenti karena kegagalan pada tahap Ekstraksi.")

if __name__ == "__main__":
    run_etl()
