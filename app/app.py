"""
Ethiopian Specialty Lot Intelligence System
Professional Dashboard for Volcafe Specialty Analyst Role
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import BASE_DIR, ETHIOPIAN_REGIONS
from src.data_loader import load_lots_data, validate_and_enrich_data
from src.utils import get_region_summary

# PAGE CONFIG 
st.set_page_config(
    page_title="Ethiopian Specialty Lot Intelligence",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("☕ Ethiopian Specialty Coffee Lot Intelligence")
st.markdown("Supporting Specialty Sourcing • Quality Control • Commercial Decisions")

# DATA LOAD 
@st.cache_data(ttl=3600)
def get_data():
    df = load_lots_data()
    return validate_and_enrich_data(df)

df = get_data()

# SIDEBAR 
st.sidebar.header("Filter Lots")

col_search = st.sidebar.columns(2)
with col_search[0]:
    search_term = st.text_input("Search Lot ID or Supplier", "")

selected_regions = st.sidebar.multiselect("Region", ETHIOPIAN_REGIONS, default=ETHIOPIAN_REGIONS)
selected_methods = st.sidebar.multiselect("Processing", df['processing_method'].unique(), default=df['processing_method'].unique())
min_score = st.sidebar.slider("Min SCA Score", 80.0, 92.0, 82.0, 0.5)
selected_grades = st.sidebar.multiselect("ECX Grade", ['Grade 1', 'Grade 2'], default=['Grade 1', 'Grade 2'])

# APPLY FILTERS
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[
        filtered_df['lot_id'].str.contains(search_term, case=False) |
        filtered_df['supplier_name'].str.contains(search_term, case=False)
    ]

filtered_df = filtered_df[
    (filtered_df['region'].isin(selected_regions)) &
    (filtered_df['processing_method'].isin(selected_methods)) &
    (filtered_df['sca_score'] >= min_score) &
    (filtered_df['grade_ecx'].isin(selected_grades))
]

# METRICS ROW 
st.subheader("Dashboard Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Filtered Lots", len(filtered_df))
with col2:
    st.metric("Avg SCA Score", f"{filtered_df['sca_score'].mean():.1f}" if not filtered_df.empty else "N/A")
with col3:
    st.metric("Total Volume", f"{filtered_df['available_quantity_kg'].sum()/1000:.1f} tons")
with col4:
    st.metric("Avg Price/kg", f"${filtered_df['price_per_kg_usd'].mean():.2f}" if not filtered_df.empty else "N/A")
with col5:
    st.metric("Grade 1 Lots", len(filtered_df[filtered_df['grade_ecx'] == 'Grade 1']))

st.divider()

# TABS
tab1, tab2, tab3, tab4 = st.tabs([" Overview", "Regional", "Lot Table", "Export"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(filtered_df, x="sca_score", color="quality_tier", 
                          title="SCA Score Distribution", nbins=12)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.pie(filtered_df, names="processing_method", title="By Processing Method")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    region_summary = get_region_summary(filtered_df)
    st.dataframe(region_summary, use_container_width=True)

    fig3 = px.bar(filtered_df.groupby("region")["sca_score"].mean().reset_index(),
                 x="region", y="sca_score", color="region",
                 title="Average Score by Region")
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    display_cols = ['lot_id', 'supplier_name', 'region', 'district', 'processing_method',
                   'sca_score', 'grade_ecx', 'defects_per_300g', 'price_per_kg_usd',
                   'traceability_level', 'sustainability_cert']

    st.dataframe(
        filtered_df.sort_values("sca_score", ascending=False)[display_cols],
        use_container_width=True,
        hide_index=True
    )

with tab4:
    st.subheader("Export Data")
    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", csv, "specialty_lots.csv", "text/csv")

    with col_exp2:
        excel_buffer = pd.ExcelWriter('specialty_lots.xlsx', engine='openpyxl')
        filtered_df.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        with open('specialty_lots.xlsx', 'rb') as f:
            st.download_button("📥 Download as Excel", f, "specialty_lots.xlsx")

st.divider()

# Footer
st.caption("**Aklilu Abera | Specialty Analyst | Built with ECX, ICO & SCA Standards**")
