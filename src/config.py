
"""
Configuration file for Ethiopian Specialty Lot Intelligence System
Aligned with ECX, ICO, SCA, and Volcafe standards.
"""

from pathlib import Path

# Project Root Detection (works whether running from notebook or script)
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RAW_DIR = DATA_DIR / "raw"

# File Paths
MOCK_DATA_CSV = DATA_DIR / "mock_data.csv"
PROCESSED_PICKLE = PROCESSED_DIR / "lots.pkl"
PROCESSED_EXCEL = PROCESSED_DIR / "lots.xlsx"

# Industry Standards & Constants
MOISTURE_MIN = 8.0
MOISTURE_MAX = 12.5
SPECIALTY_SCA_THRESHOLD = 80.0
ECX_GRADE1_MAX_DEFECTS = 3
ECX_GRADE2_MAX_DEFECTS = 12

# Standard Lists
ETHIOPIAN_REGIONS = ["Yirgacheffe", "Sidama", "Guji", "Limmu", "Kaffa", "Bench Maji"]
PROCESSING_METHODS = ["Washed", "Natural", "Honey"]
TRACEABILITY_LEVELS = ["Full", "Washing Station", "Exporter"]
SUSTAINABILITY_CERTS = ["Organic", "Volcafe Verified", "Rainforest Alliance", "None"]
GRADES_ECX = ["Grade 1", "Grade 2"]

print("Configuration loaded successfully!")
print(f"Project Root: {BASE_DIR}")
