import pandas as pd;


'''
# 1. Load the raw data, skipping Stat-Xplore headers
df = pd.read_csv(r"data\table_20     *  -07-22_13-09-16.csv", skiprows=9)
df = df.iloc[:, :-1]
df.columns = ['Counting', 'Ward', 'Employment_Indicator', 'Month', 'Count', 'Annotations']

# 2. Clean out metadata footers and borough-level totals
df = df.dropna(subset=['Ward'])
df = df[~df['Ward'].isin(['Camden', 'Total'])]
valid_wards = [w for w in df['Ward'].unique() if len(w) < 40]
df = df[df['Ward'].isin(valid_wards)]

# 3. Handle the suppressed Feb 2026 data ('..') and cast to integer
df['Count'] = pd.to_numeric(df['Count'], errors='coerce').fillna(0).astype(int)
#  +4. Filter down to the essential columns
df = df[['Ward', 'Employment_Indicator', 'Month', 'Count']]

# 5. Export to a clean CSV ready for PostgreSQL bulk insert
df.to_csv('cleaned_universal_credit_ward.csv', index=False)
print(f"Pipeline complete. Exported {df.shape[0]} rows.")
'''
FILEPATH = r"data/UC_london.csv"
 
df = pd.read_csv(FILEPATH, skiprows=9)  # adjust skiprows once you check for title rows above the header
 
df.columns = [c.strip() for c in df.columns]
df = df.rename(columns={
    "National - Regional - LA - OAs": "local_authority",   # adjust to the exact full column name -- yours is truncated in the screenshot
    "Employment Indicator (V)": "employment_indicator",
    "Count": "count",
})
 
# Suppressed/non-numeric markers -- flag before converting, don't silently drop
df["suppressed"] = df["count"].astype(str).str.strip().isin(["-", "*", "c", "..", "x", "X"])
df["count"] = pd.to_numeric(
    df["count"].astype(str).str.replace(",", "", regex=False).where(~df["suppressed"]),
    errors="coerce",
)
 
# Some months are marked "(rev)" -- a revised figure alongside/instead of
# the originally published one. Flag it, then strip it so the date parses.
df["is_revised"] = df["Month"].str.contains(r"\(rev\)", na=False)
df["month_clean"] = df["Month"].str.replace(r"\s*\(rev\)", "", regex=True).str.strip()
df["month_date"] = pd.to_datetime(df["month_clean"], format="%B %Y")
 
# If a month appears twice (original + revised), keep the revised one --
# it's the more accurate figure. Sort so revised rows come last, then drop
# duplicates keeping the last (revised) occurrence per LA/employment/month.
df = df.sort_values("is_revised")
df = df.drop_duplicates(subset=["local_authority", "employment_indicator", "month_date"], keep="last")
 
# THE IMPORTANT PART: this file is monthly (same shape as the Camden ward bug).
# Don't sum across months. Keep only the latest month per borough/employment status.
latest_month = df["month_date"].max()
df_latest = df[df["month_date"] == latest_month].copy()
df_latest.to_csv("uc_london_latest_month.csv", index=False)
df.to_csv("uc_london_full_timeseries.csv", index=False) 

print(f"Latest month in data: {latest_month.strftime('%b-%y')}")
print(df_latest[["local_authority", "employment_indicator", "count"]].head(10))
