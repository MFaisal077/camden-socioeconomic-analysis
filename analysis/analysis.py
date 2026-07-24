"""
MVP vulnerability score. Pulls from Postgres, scores in pandas, exports CSV.

Logic: normalize each signal to a z-score (so different scales/units don't
distort things), then sum them into one composite score per local authority.
Higher score = more vulnerability signals stacking up in the same place.

Run: python mvp_vulnerability_score.py
"""

import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine


DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "Faisal@123"
DB_PORT = "5432"
DB_NAME = "camden_welfare_db"

encoded_password = quote_plus(DB_PASSWORD)
engine = create_engine(f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")



uc = pd.read_sql("""
    SELECT borough, SUM(uc_claimants) AS total_uc_claimants
    FROM fact_universal_credit
    GROUP BY borough 
""", engine)

foodbank = pd.read_sql("""
    SELECT local_authority, "Total parcels distributed"
    FROM fact_foodbank_parcels
    WHERE year = (SELECT MAX(year) FROM fact_foodbank_parcels)
""", engine)

ctax = pd.read_sql("""
    SELECT "Local Authority", "Count" AS ctax_reduction_claimants
    FROM fact_council_tax_reduction
    WHERE "Quarter" = (SELECT MAX("Quarter") FROM fact_council_tax_reduction)  
""", engine)



df = uc.merge(foodbank, on="local_authority", how="inner") \
        .merge(ctax, on="Local Authority", how="inner")



for col in ["total_uc_claimants", "total_parcels_distributed", "ctax_reduction_claimants"]:
    df[f"{col}_z"] = (df[col] - df[col].mean()) / df[col].std()

df["vulnerability_score"] = (
    df["total_uc_claimants_z"] + df["total_parcels_distributed_z"] + df["ctax_reduction_claimants_z"]
)

df = df.sort_values("vulnerability_score", ascending=False).reset_index(drop=True)

# --- Output ---

print(df[["Local Authority", "vulnerability_score"]].head(15).to_string(index=False))

camden_row = df[df["Local Authority"].str.contains("Camden", case=False, na=False)]
if not camden_row.empty:
    rank = camden_row.index[0] + 1
    print(f"\nCamden rank: {rank} of {len(df)}")

#df.to_csv("vulnerability_scores.csv", index=False)
#print("\n✔ Saved to vulnerability_scores.csv")