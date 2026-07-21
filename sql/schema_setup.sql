-- =========================================================================
-- Camden Council Scheme & Provision Data Analysis - Database Schema
-- =========================================================================

-- 1. Drop existing tables safely to allow for clean pipeline rebuilds
DROP TABLE IF EXISTS fact_housing_stock CASCADE;
DROP TABLE IF EXISTS dim_estates CASCADE;
DROP TABLE IF EXISTS dim_lsoa_deprivation CASCADE;
DROP TABLE IF EXISTS fact_universal_credit CASCADE;
DROP TABLE IF EXISTS fact_housing_benefit CASCADE;

-- =========================================================================
-- 2. Create Dimension Tables
-- =========================================================================

-- Dimension Table: Council Estates
CREATE TABLE dim_estates (
    estate_name VARCHAR(255) PRIMARY KEY,
    count_of_tenanted_properties INT NOT NULL,
    easting VARCHAR(50),
    northing VARCHAR(50),
    location VARCHAR(255)
);

-- Dimension Table: LSOA Deprivation & Barriers
CREATE TABLE dim_lsoa_deprivation (
    lsoa21cd VARCHAR(20) PRIMARY KEY,
    lsoa21nm VARCHAR(100) NOT NULL,
    cleaned_ward VARCHAR(100) NOT NULL,
    income_score NUMERIC(5, 4),
    income_rank INT,
    income_decile INT,
    barriers_to_housing_and_services_score NUMERIC(6, 3),
    barriers_to_housing_and_services_rank INT,
    living_environment_score NUMERIC(6, 3)
);

-- =========================================================================
-- 3. Create Fact Tables
-- =========================================================================

-- Fact Table: Housing Stock
CREATE TABLE fact_housing_stock (
    property_reference VARCHAR(50) PRIMARY KEY,
    property_type VARCHAR(100),
    property_subtype VARCHAR(100),
    bedroom_count INT,
    estate_name VARCHAR(255),
    cleaned_ward VARCHAR(100),
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6),
    CONSTRAINT fk_housing_estate FOREIGN KEY (estate_name) 
        REFERENCES dim_estates(estate_name) ON DELETE SET NULL
);

-- Fact Table: Universal Credit Time-Series (DWP)
CREATE TABLE fact_universal_credit (
    id SERIAL PRIMARY KEY,
    borough VARCHAR(100) NOT NULL,
    month VARCHAR(50) NOT NULL,
    uc_claimants INT NOT NULL
);

-- Fact Table: Housing Benefit Time-Series (DWP)
CREATE TABLE fact_housing_benefit (
    id SERIAL PRIMARY KEY,
    borough VARCHAR(100) NOT NULL,
    month VARCHAR(50) NOT NULL,
    hb_claimants INT NOT NULL
);

-- =========================================================================
-- 4. Create Indexes for Dashboard Performance Optimization
-- =========================================================================
CREATE INDEX idx_housing_ward ON fact_housing_stock(cleaned_ward);
CREATE INDEX idx_housing_estate ON fact_housing_stock(estate_name);
CREATE INDEX idx_lsoa_ward ON dim_lsoa_deprivation(cleaned_ward);
CREATE INDEX idx_uc_month ON fact_universal_credit(month);