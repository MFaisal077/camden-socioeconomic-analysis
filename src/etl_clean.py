import os
import pandas as pd
import numpy as np

DATA_DIR = "data"

def clean_ward_name(name):
    if pd.isna(name):
        return 'Unknown'
    name = str(name).replace(' Ward', '').replace(' ward', '').strip()
    if name in ['Holborn and Covent Garden', 'Holborn & Covent Garden']:
        return 'Holborn & Covent Garden'
    if name in ['Regents Park', "Regent's Park"]:
        return "Regent's Park"
    if name in ['Kings Cross', "King's Cross"]:
        return "King's Cross"
    return name

def run_cleaning():
    print("Running Phase 1: Data Cleaning...")

    # Load raw datasets
    housing_raw = pd.read_csv(os.path.join(DATA_DIR, 'Camden_Housing_Stock_20260721.csv'))
    export_raw = pd.read_csv(os.path.join(DATA_DIR, 'export.csv'))
    uc_raw = pd.read_csv(os.path.join(DATA_DIR, 'UC.csv'), skiprows=9).dropna(subset=['Count'])
    hb_raw = pd.read_csv(os.path.join(DATA_DIR, 'HB.csv'), skiprows=9).dropna(subset=['Count'])
    
    xls = pd.ExcelFile(os.path.join(DATA_DIR, 'jsna_data_download.xlsx'))
    lsoa_dep_raw = pd.read_excel(xls, 'IOD - LSOA')

    # 1. Clean Housing Stock (Matches fact_housing_stock schema)
    housing_clean = housing_raw.copy()
    housing_clean['cleaned_ward'] = housing_clean['Ward Name'].apply(clean_ward_name)
    housing_clean['bedroom_count'] = pd.to_numeric(housing_clean['Bedroom Count'], errors='coerce').fillna(0).astype(int)
    housing_clean['property_type'] = housing_clean['Property Type'].str.strip().fillna('Unknown')
    housing_clean['property_subtype'] = housing_clean['Property Subtype'].str.strip()
    housing_clean['property_reference'] = housing_clean['Property Reference'].astype(str)
    housing_clean['estate_name'] = housing_clean['Estate Name'].str.strip()
    
    housing_clean = housing_clean[[
        'property_reference', 'property_type', 'property_subtype', 
        'bedroom_count', 'estate_name', 'cleaned_ward', 'Latitude', 'Longitude'
    ]]
    housing_clean.columns = [
        'property_reference', 'property_type', 'property_subtype', 
        'bedroom_count', 'estate_name', 'cleaned_ward', 'latitude', 'longitude'
    ]

    # 2. Clean Estates (Matches dim_estates schema)
    export_clean = export_raw.copy()
    export_clean['estate_name'] = export_clean['Estate Name'].str.strip()
    export_clean['count_of_tenanted_properties'] = pd.to_numeric(export_clean['Count of tenanted properties'], errors='coerce').fillna(0).astype(int)
    
    export_clean = export_clean[['estate_name', 'count_of_tenanted_properties', 'Easting', 'Northing', 'Location']]
    export_clean.columns = ['estate_name', 'count_of_tenanted_properties', 'easting', 'northing', 'location']

    # 3. Clean Universal Credit (Matches fact_universal_credit schema)
    uc_clean = uc_raw.copy()
    uc_clean['Month'] = uc_clean['Month'].str.strip()
    uc_clean['Count'] = uc_clean['Count'].astype(float).astype(int)
    
    uc_clean = uc_clean[['National - Regional - LA - OAs', 'Month', 'Count']]
    uc_clean.columns = ['borough', 'month', 'uc_claimants']

    # 4. Clean Housing Benefit (Matches fact_housing_benefit schema)
    hb_clean = hb_raw.copy()
    hb_clean['Month'] = hb_clean['Month'].str.strip()
    hb_clean['Count'] = hb_clean['Count'].astype(float).astype(int)
    
    hb_clean = hb_clean[['National - Regional - Admin LA (I, II, XVIII, XXIII)', 'Month', 'Count']]
    hb_clean.columns = ['borough', 'month', 'hb_claimants']

    # 5. Clean LSOA Deprivation (Matches dim_lsoa_deprivation schema)
    lsoa_clean = lsoa_dep_raw.copy()
    lsoa_clean['cleaned_ward'] = lsoa_clean['wd22nm'].apply(clean_ward_name)
    
    lsoa_clean = lsoa_clean[[
        'lsoa21cd', 'lsoa21nm', 'cleaned_ward', 
        'Income Score', 'Income Rank', 'Income Decile', 
        'Barriers to Housing and Services Score', 
        'Barriers to Housing and Services Rank', 
        'Living Environment Score'
    ]]
    lsoa_clean.columns = [
        'lsoa21cd', 'lsoa21nm', 'cleaned_ward', 
        'income_score', 'income_rank', 'income_decile', 
        'barriers_to_housing_and_services_score', 
        'barriers_to_housing_and_services_rank', 
        'living_environment_score'
    ]

    # Save outputs to data/ folder
    os.makedirs(DATA_DIR, exist_ok=True)
    housing_clean.to_csv(os.path.join(DATA_DIR, 'cleaned_housing_stock.csv'), index=False)
    export_clean.to_csv(os.path.join(DATA_DIR, 'cleaned_estates.csv'), index=False)
    uc_clean.to_csv(os.path.join(DATA_DIR, 'cleaned_universal_credit.csv'), index=False)
    hb_clean.to_csv(os.path.join(DATA_DIR, 'cleaned_housing_benefit.csv'), index=False)
    lsoa_clean.to_csv(os.path.join(DATA_DIR, 'cleaned_lsoa_deprivation.csv'), index=False)

    print("Phase 1 Complete: Cleaned datasets successfully exported with schema-matching columns.")

if __name__ == "__main__":
    run_cleaning()