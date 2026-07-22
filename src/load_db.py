import os
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text


DATA_DIR = "data"
DB_USER = "postgres"
DB_PASSWORD = "Faisal@123"  
DB_PORT = "5432"
DB_NAME = "camden_welfare_db"

def load_to_postgresql():
    print("Running Phase 2: Loading data into PostgreSQL...")

    
    encoded_password = quote_plus(DB_PASSWORD)
    db_connection_str = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(db_connection_str)


    print("Dropping existing tables with CASCADE...")
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS fact_housing_stock CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS dim_estates CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS dim_lsoa_deprivation CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_universal_credit CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_housing_benefit CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_universal_credit_ward CASCADE;"))

    # 2. Load cleaned CSV files
    housing_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_housing_stock.csv'))
    export_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_estates.csv'))
    uc_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_universal_credit.csv'))
    hb_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_housing_benefit.csv'))
    lsoa_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_lsoa_deprivation.csv'))
    universal_clean_ward=pd.read_csv(os.path.join(DATA_DIR, 'cleaned_universal_credit_ward.csv'))

    # 3. Insert fresh data into PostgreSQL tables
    print("Inserting data into database tables...")
    export_clean.to_sql('dim_estates', engine, if_exists='replace', index=False, method='multi')
    lsoa_clean.to_sql('dim_lsoa_deprivation', engine, if_exists='replace', index=False, method='multi')
    housing_clean.to_sql('fact_housing_stock', engine, if_exists='replace', index=False, method='multi')
    uc_clean.to_sql('fact_universal_credit', engine, if_exists='replace', index=False, method='multi')
    hb_clean.to_sql('fact_housing_benefit', engine, if_exists='replace', index=False, method='multi')
    universal_clean_ward.to_sql('fact_universal_ward_credit', engine, if_exists='replace', index=False, method='multi')

    print("Phase 2 Complete: All tables successfully populated in PostgreSQL!")

if __name__ == "__main__":
    load_to_postgresql()