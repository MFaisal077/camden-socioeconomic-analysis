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
        conn.execute(text("DROP VIEW IF EXISTS population CASCADE;"))

    # 2. Load cleaned CSV files
    population_clean = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_population.csv'))


    # 3. Insert fresh data into PostgreSQL tables
    print("Inserting data into database tables...")
    population_clean.to_sql('population', engine, if_exists='replace', index=False, method='multi')

    # 4. Post-insert verification query placed inside the function


    print("Phase 2 Complete: All tables successfully populated in PostgreSQL!")

if __name__ == "__main__":
    load_to_postgresql()