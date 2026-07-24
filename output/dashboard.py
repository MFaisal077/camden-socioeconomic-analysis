import streamlit as st
import pandas as pd
import sqlalchemy

# 1. Page Configuration
st.set_page_config(
    page_title="Camden Welfare & Financial Distress MVP",
    page_icon="",
    layout="wide"
)


@st.cache_resource
def get_connection():
    # Format: postgresql://username:password@host:port/database_name
    engine = sqlalchemy.create_engine('postgresql://postgres:Faisal%40123@localhost:5432/camden_welfare_db')
    return engine

engine = get_connection()


@st.cache_data
def load_data():
    df_distress = pd.read_sql("SELECT * FROM vw_ward_financial_distress", engine)
    df_foodbank = pd.read_sql("SELECT * FROM fact_foodbank_parcels WHERE year = 2024", engine)
    return df_distress, df_foodbank

df_distress, df_foodbank = load_data()


st.title("Local Authority Financial Vulnerability MVP")
st.markdown("Real-time pipeline merging Universal Credit, employment indicators, and emergency support metrics.")


col1, col2, col3 = st.columns(3)
total_claimants = df_distress["claimant_volume"].sum()
total_wards = df_distress["ward_name"].nunique()
total_parcels = df_foodbank["total_parcels_distributed"].sum() if "total_parcels_distributed" in df_foodbank.columns else 0

col1.metric("Total Tracked Claimants", f"{total_claimants:,.0f}")
col2.metric("Wards Analyzed", f"{total_wards}")
col3.metric("Food Bank Parcels (2024)", f"{total_parcels:,.0f}")

st.markdown("---")


st.subheader("Ward-Level Financial Distress Breakdown")


ward_summary = df_distress.groupby("ward_name")["claimant_volume"].sum().reset_index()
ward_summary = ward_summary.sort_values(by="claimant_volume", ascending=False)


st.bar_chart(ward_summary.set_index("ward_name"))


with st.expander("🔍 View Raw Underlying Data Table"):
    st.dataframe(df_distress)