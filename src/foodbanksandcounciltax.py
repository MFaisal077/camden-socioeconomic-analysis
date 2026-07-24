import pandas as pd;
import numpy as np;


ct_reductions=pd.read_csv(r"data\Local_Council_Tax_Support_Claimants_Live_Table_Q4_2025-26.csv",skiprows=3)

ct_reductions= ct_reductions.drop(columns=["Notes","Percentage Change (%) from Q4 2024-2025 to Q4 2025-2026","Percentage Change (%) from Q3 2025-2026 to Q4 2025-2026"])
ct_reductions.columns = [
    col.replace("As at ", "").strip() if "As at" in col else col 
    for col in ct_reductions.columns
]
ct_reductions=ct_reductions.replace({',': ''}, regex=True)
ct_reductions=pd.melt(ct_reductions,id_vars=['E-code', 'ONS Code', 'Local Authority', 'Class', 'Region'],
    var_name='Quarter',
    value_name='Count')

ct_reductions['Count'] = ct_reductions['Count'].replace(['-', 'x', 'X', ' ', '','[x]','[z]'], np.nan)
ct_reductions=ct_reductions.dropna(subset=['Count'])
#print(ct_reductions.head(10))

#ct_reductions.to_csv(r"data/cleaned_council_tax_reductions.csv",index=False)

FILEPATH = "data\eys_2025_parcel_stats(Local authority).csv"


 
raw = pd.read_csv(FILEPATH, header=None)
 
year_row = raw.iloc[0].copy()
year_row.iloc[3:] = year_row.iloc[3:].ffill()   # fill merged year cells
subheader_row = raw.iloc[1]
 
cols = []
for i in range(len(raw.columns)):
    if i < 3:
        cols.append(str(raw.iloc[0, i]).strip())
    else:
        cols.append(f"{str(year_row.iloc[i]).strip()}_{str(subheader_row.iloc[i]).strip()}")
 
df = raw.iloc[2:].copy()
df.columns = cols
df = df.rename(columns={"Local Authority": "local_authority", "Nation": "nation", "Region": "region"})
 
id_cols = ["nation", "local_authority", "region"]
df_long = df.melt(id_vars=id_cols, var_name="year_metric", value_name="value")
 
split = df_long["year_metric"].str.split("_", n=1, expand=True)
df_long["year"] = pd.to_numeric(split[0], errors="coerce")
df_long["metric"] = split[1].str.strip()
 
df_long["no_foodbank_operating"] = df_long["value"].astype(str).str.strip().eq("-")
df_long["value"] = pd.to_numeric(
    df_long["value"].astype(str).str.replace(",", "", regex=False).where(~df_long["no_foodbank_operating"]),
    errors="coerce",
)
 
df_clean = df_long.pivot_table(
    index=id_cols + ["year", "no_foodbank_operating"],
    columns="metric", values="value", aggfunc="first",
).reset_index()
df_clean.columns.name = None
 
df_clean.to_csv("foodbank_clean.csv", index=False)
print(df_clean)
 