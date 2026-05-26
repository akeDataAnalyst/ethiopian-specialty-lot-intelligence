
"""
Data loading, saving, and basic processing module.
"""

import pandas as pd
from pathlib import Path
import sys
import os

# === FIX: Add project root to Python path ===
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now import config
from src.config import (
    MOCK_DATA_CSV, 
    PROCESSED_PICKLE,
    SPECIALTY_SCA_THRESHOLD
)


def load_lots_data() -> pd.DataFrame:
    """Load data with priority: Pickle → CSV"""
    if PROCESSED_PICKLE.exists():
        df = pd.read_pickle(PROCESSED_PICKLE)
        print(f"Loaded from pickle: {len(df)} lots")
    elif MOCK_DATA_CSV.exists():
        df = pd.read_csv(MOCK_DATA_CSV)
        if 'arrival_date' in df.columns:
            df['arrival_date'] = pd.to_datetime(df['arrival_date'])
        if 'last_updated' in df.columns:
            df['last_updated'] = pd.to_datetime(df['last_updated'])
        print(f"Loaded from CSV: {len(df)} lots")
    else:
        raise FileNotFoundError("No data file found. Please run Phase 1 first.")

    return df


def save_processed_data(df: pd.DataFrame) -> None:
    """Save processed data"""
    PROCESSED_PICKLE.parent.mkdir(parents=True, exist_ok=True)
    df.to_pickle(PROCESSED_PICKLE)
    print(f"Processed data saved to: {PROCESSED_PICKLE}")


def validate_and_enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply quality rules and enrich dataset"""
    df = df.copy()

    df['is_specialty'] = df['sca_score'] >= SPECIALTY_SCA_THRESHOLD

    df['quality_tier'] = pd.cut(
        df['sca_score'],
        bins=[0, 82, 85, 88, 100],
        labels=['Good', 'Very Good', 'Excellent', 'Outstanding']
    )

    df['ecx_compliant'] = (
        ((df['grade_ecx'] == 'Grade 1') & (df['defects_per_300g'] <= 3)) |
        ((df['grade_ecx'] == 'Grade 2') & (df['defects_per_300g'] <= 12))
    )

    return df
