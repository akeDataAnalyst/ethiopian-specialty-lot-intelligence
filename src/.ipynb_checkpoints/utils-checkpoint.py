
"""
Utility functions for analysis and formatting.
"""

import pandas as pd


def get_region_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summary statistics by region"""
    return df.groupby('region').agg({
        'sca_score': ['mean', 'max', 'min', 'count'],
        'available_quantity_kg': 'sum',
        'price_per_kg_usd': 'mean',
        'is_specialty': 'sum'
    }).round(2)


def filter_by_criteria(df: pd.DataFrame, min_score: float = 80.0, region: str = None):
    """Filter lots based on criteria"""
    filtered = df[df['sca_score'] >= min_score].copy()
    if region:
        filtered = filtered[filtered['region'] == region]
    return filtered


def format_quantity(kg: float) -> str:
    """Nice quantity formatting"""
    if kg >= 1000:
        return f"{kg/1000:.1f} tons"
    else:
        return f"{int(kg)} kg"
