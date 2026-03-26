from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# Request
CATEGORIES = Literal["OPEN", "OBC-NCL", "SC", "ST", "EWS"]
COLLEGE_TYPES = Literal["IIT", "NIT", "IIIT", "GFTI", "ALL"]
GENDERS = Literal["Gender-Neutral", "Female-only"]

class PredictRequest(BaseModel):
    rank: int = Field(..., gt=0, description="Category Rank (e.g. your rank in EWS, or CRL in OPEN)")
    category: CATEGORIES = Field(default="OPEN")
    college_type: COLLEGE_TYPES = Field(default="ALL")
    gender: GENDERS = Field(default="Gender-Neutral")
    home_state: Optional[str] = Field(default=None)
    include_five_year: bool = Field(default=True)

# Response
class CollegeResult(BaseModel):
    institute: str
    program: str
    branch: str
    program_type: str  # BTech, Integrated, etc.
    college_type: str  # IIT, NIT, IIIT, GFTI
    quota: str         # AI, HS, OS
    seat_type: str
    gender: str
    opening_rank: int
    closing_rank: int
    rank_gap: int
    priority: int      # 1=IIT, 2=NIT, 3=IIIT, 4=GFTI

class PredictResponse(BaseModel):
    rank: int
    category: str
    college_type: str
    total_results: int
    results: List[CollegeResult]
