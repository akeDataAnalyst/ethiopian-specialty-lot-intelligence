
"""
Pydantic models for data validation and type safety.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CoffeeLot(BaseModel):
    lot_id: str
    supplier_name: str
    washing_station: str
    region: str
    district: str
    processing_method: str
    harvest_year: int
    harvest_period: str
    arrival_date: datetime
    grade_ecx: str
    defects_per_300g: int = Field(ge=0)
    moisture_pct: float = Field(ge=8.0, le=12.5)
    water_activity: float
    sca_score: float = Field(ge=70.0, le=100.0)
    flavor_profile: str
    cup_notes: Optional[str] = None
    quantity_bags: int = Field(gt=0)
    available_quantity_kg: float
    price_per_kg_usd: float = Field(gt=0)
    traceability_level: str
    sustainability_cert: str
    status: str
    last_updated: datetime
    is_specialty: bool = False

    class Config:
        arbitrary_types_allowed = True
