"""
Ethiopian Specialty Lot Intelligence System
Interactive Dashboard for Volcafe Specialty Analyst
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import BASE_DIR, ETHIOPIAN_REGIONS
from src.data_loader import load_lots_data, validate_and_enrich_data
from src.utils import get_region_summary

# PAGE CONFIG
st.set_page_config(
    page_title="Ethiopian Specialty Lots | Volcafe",
    page_icon="☕",
    layout="wide"
)

st.title("☕ Ethiopian Specialty Coffee Lot Intelligence")
st.markdown("**Supporting Specialty Sourcing • Quality Control • Commercial Decisions**")

# LOAD DATA
@st.cache_data
def get_data():
    df = load_lots_data()
    df = validate_and_enrich_data(df)
    return df

df = get_data()

# SIDEBAR FILTERS
st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Region", 
    options=ETHIOPIAN_REGIONS,
    default=ETHIOPIAN_REGIONS
)

selected_processing = st.sidebar.multiselect(
    "Processing Method",
    options=df['processing_method'].unique(),
    default=df['processing_method'].unique()
)

min_score = st.sidebar.slider(
    "Minimum SCA Score", 
    min_value=80.0, 
    max_value=92.0, 
    value=82.0, 
    step=0.5
)

selected_grade = st.sidebar.multiselect(
    "ECX Grade",
    options=['Grade 1', 'Grade 2'],
    default=['Grade 1', 'Grade 2']
)

# Apply filters
filtered_df = df[
    (df['region'].isin(selected_regions)) &
    (df['processing_method'].isin(selected_processing)) &
    (df['sca_score'] >= min_score) &
    (df['grade_ecx'].isin(selected_grade))
]

# METRICS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Lots", len(filtered_df))
with col2:
    st.metric("Avg SCA Score", f"{filtered_df['sca_score'].mean():.1f}")
with col3:
    st.metric("Total Quantity", f"{filtered_df['available_quantity_kg'].sum()/1000:.1f} tons")
with col4:
    st.metric("Avg Price", f"${filtered_df['price_per_kg_usd'].mean():.2f}/kg")

st.divider()

# VISUALIZATIONS
tab1, tab2, tab3 = st.tabs(["Overview", "Regional Analysis", "Detailed Lots"])

with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        fig = px.histogram(filtered_df, x='sca_score', nbins=15, 
                          title="SCA Score Distribution",
                          color='quality_tier')
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = px.pie(filtered_df, names='processing_method', 
                     title="Lots by Processing Method")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    region_sum = get_region_summary(filtered_df)
    st.dataframe(region_sum, use_container_width=True)

    fig3 = px.bar(
        filtered_df.groupby('region')['sca_score'].mean().reset_index(),
        x='region', y='sca_score',
        title="Average SCA Score by Region",
        color='region'
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    # Sort by score
    display_cols = ['lot_id', 'supplier_name', 'region', 'processing_method', 
                   'sca_score', 'grade_ecx', 'defects_per_300g', 
                   'price_per_kg_usd', 'traceability_level']

    st.dataframe(
        filtered_df.sort_values('sca_score', ascending=False)[display_cols],
        use_container_width=True,
        hide_index=True
    )

# FOOTER
st.caption("**Aklilu Abera | Specialty Analyst | Built with ECX, ICO & SCA Standards**")
