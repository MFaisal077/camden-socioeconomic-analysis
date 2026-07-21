-- =========================================================================
-- Camden Council Scheme & Provision - Power BI Analytical Views
-- =========================================================================

-- View 1: Ward-Level Vulnerability & Scheme Priority Ranking
CREATE OR REPLACE VIEW vw_ward_vulnerability_summary AS
SELECT 
    l.cleaned_ward AS ward_name,
    COUNT(h.property_reference) AS total_council_properties,
    ROUND(AVG(l.income_score)::numeric, 3) AS average_income_deprivation,
    ROUND(AVG(l.barriers_to_housing_and_services_score)::numeric, 2) AS housing_barriers_score,
    -- Composite Score combining property density and income deprivation
    ROUND((COUNT(h.property_reference) * 0.4 + AVG(l.income_score) * 100 * 0.6)::numeric, 2) AS scheme_priority_index
FROM dim_lsoa_deprivation l
LEFT JOIN fact_housing_stock h ON l.cleaned_ward = h.cleaned_ward
GROUP BY l.cleaned_ward
ORDER BY scheme_priority_index DESC;

-- View 2: Top Council Estates by Target Density
CREATE OR REPLACE VIEW vw_top_estates_density AS
SELECT 
    estate_name,
    count_of_tenanted_properties,
    easting,
    northing,
    location
FROM dim_estates
ORDER BY count_of_tenanted_properties DESC;

-- View 3: Universal Credit & Welfare Trajectory (Time-Series Trends)
CREATE OR REPLACE VIEW vw_welfare_time_series AS
SELECT 
    month,
    uc_claimants,
    LAG(uc_claimants, 1) OVER (ORDER BY month) AS previous_month_claimants,
    uc_claimants - LAG(uc_claimants, 1) OVER (ORDER BY month) AS monthly_change
FROM fact_universal_credit
ORDER BY month;