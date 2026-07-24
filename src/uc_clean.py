import pandas as pd;



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