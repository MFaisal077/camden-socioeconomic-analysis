import os
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

DATA_DIR = "data"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PASSWORD = "Faisal@123"  
DB_PORT = "5432"
DB_NAME = "camden_welfare_db"

def load_to_postgresql():
    print("Running Phase 2: Loading data into PostgreSQL...")

    encoded_password = quote_plus(DB_PASSWORD)
    db_connection_str = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(db_connection_str)

    print("Dropping existing tables and views with CASCADE...")
    with engine.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS vw_ward_financial_distress CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_housing_stock CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS dim_estates CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS dim_lsoa_deprivation CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_universal_credit CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_housing_benefit CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_universal_ward_credit CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_foodbank_parcels CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fact_council_tax_reduction CASCADE;"))

    # 2. Load cleaned CSV files
    housing_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_housing_stock.csv'))
    export_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_estates.csv'))
    uc_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_universal_credit.csv'))
    hb_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_housing_benefit.csv'))
    lsoa_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_lsoa_deprivation.csv'))
    universal_clean_ward = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_universal_credit_ward.csv'))
    foodbank_clean = pd.read_csv(os.path.join(DATA_DIR, 'foodbank_clean.csv'))
    ctax_reduction_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_council_tax_reductions.csv'))

    print("--- Pre-Insert Check ---")
    print(f"universal_clean_ward rows: {len(universal_clean_ward)}")
    print(f"foodbank_clean rows: {len(foodbank_clean)}")

    print("Sample ward columns:", universal_clean_ward.columns.tolist()[:3])
    print("Sample foodbank columns:", foodbank_clean.columns.tolist()[:3])

    # 3. Insert fresh data into PostgreSQL tables
    print("Inserting data into database tables...")
    export_clean.to_sql('dim_estates', engine, if_exists='replace', index=False, method='multi')
    lsoa_clean.to_sql('dim_lsoa_deprivation', engine, if_exists='replace', index=False, method='multi')
    housing_clean.to_sql('fact_housing_stock', engine, if_exists='replace', index=False, method='multi')
    uc_clean.to_sql('fact_universal_credit', engine, if_exists='replace', index=False, method='multi')
    hb_clean.to_sql('fact_housing_benefit', engine, if_exists='replace', index=False, method='multi')
    universal_clean_ward.to_sql('fact_universal_ward_credit', engine, if_exists='replace', index=False, method='multi')
    foodbank_clean.to_sql('fact_foodbank_parcels', engine, if_exists='replace', index=False, method='multi')
    ctax_reduction_clean.to_sql('ctax_support', engine, if_exists='replace', index=False, method='multi')

    # 4. Post-insert verification query placed inside the function
    with engine.connect() as conn:
        res_ward = conn.execute(text("SELECT COUNT(*) FROM fact_universal_ward_credit;")).scalar()
        res_fb = conn.execute(text("SELECT COUNT(*) FROM fact_foodbank_parcels;")).scalar()
        print(f"PostgreSQL Table 'fact_universal_ward_credit' row count: {res_ward}")
        print(f"PostgreSQL Table 'fact_foodbank_parcels' row count: {res_fb}")

    print("Phase 2 Complete: All tables successfully populated in PostgreSQL!")

if __name__ == "__main__":
    load_to_postgresql()