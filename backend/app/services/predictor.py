"""
Core prediction service supporting real multi-file JOSAA dataset and GFTIs.
"""
from __future__ import annotations

from typing import Any
import pandas as pd

from app.models.schema import CollegeResult, PredictRequest, PredictResponse
from app.utils.college_classifier import CollegeType, classify_institute, get_quota_for_institute
from app.utils.program_parser import extract_branch_name, get_program_type, is_five_year_program
from app.utils.data_loader import load_josaa_data

# Priority constants
_PRIORITY: dict[str, int] = {
    CollegeType.IIT: 1,
    CollegeType.NIT: 2,
    CollegeType.IIIT: 3,
    CollegeType.GFTI: 4,
    CollegeType.OTHER: 5,
}

TOP_N = 25

def predict_colleges(request: PredictRequest) -> PredictResponse:
    df = load_josaa_data()
    
    # 1. Base Integrity: Remove NaN closing ranks
    df = df.dropna(subset=['closing_rank'])
    
    # 2. Vectorized exact matches (Massively speeds up subsetting)
    cat_mask = df['seat_type'].str.strip().str.upper() == request.category.strip().upper()
    gender_mask = df['gender'].str.strip().str.lower() == request.gender.strip().lower()
    df = df[cat_mask & gender_mask].copy()

    # 3. Compute rank_gap and Apply deterministic margin filter
    df['closing_rank'] = df['closing_rank'].astype(int)
    df['rank_gap'] = df['closing_rank'] - request.rank
    
    # Filter out anything below -100 gap
    df = df[df['rank_gap'] >= -100]

    # Stop early if empty
    if df.empty:
        return PredictResponse(rank=request.rank, category=request.category, college_type=request.college_type, total_results=0, results=[])

    # 4. Apply custom python logic logic on the deeply filtered subset
    results: list[CollegeResult] = []
    for _, row in df.iterrows():
        institute = str(row.get("institute", ""))
        program_name = str(row.get("academic_program_name", ""))
        row_quota = str(row.get("quota", "")).strip().upper()
        
        # Five year check
        if not request.include_five_year and is_five_year_program(program_name):
            continue
            
        # College type check
        ctype = classify_institute(institute)
        if request.college_type != "ALL" and ctype.value != request.college_type:
            continue
            
        # Quota logic (HS vs AI/OS)
        valid_quotas = [q.upper() for q in get_quota_for_institute(institute, request.home_state)]
        if row_quota not in valid_quotas:
            continue
            
        # Chance categorization
        gap = int(row['rank_gap'])
        if gap >= 200:
            chance = "Safe"
        elif 0 <= gap < 200:
            chance = "Moderate"
        elif -100 <= gap < 0:
            chance = "Dream"
        else:
            continue

        opening = row.get("opening_rank", 0)
        
        results.append(CollegeResult(
            institute=institute,
            program=program_name,
            branch=extract_branch_name(program_name),
            program_type=get_program_type(program_name),
            college_type=ctype.value,
            quota=row_quota,
            seat_type=str(row['seat_type']).strip().upper(),
            gender=str(row['gender']).strip(),
            opening_rank=int(opening) if not pd.isna(opening) else 0,
            closing_rank=int(row['closing_rank']),
            rank_gap=gap,
            chance_category=chance,
            priority=_PRIORITY.get(ctype, 5)
        ))

    # 5. Sorting logic
    chance_map = {"Safe": 1, "Moderate": 2, "Dream": 3}
    results.sort(key=lambda x: (chance_map[x.chance_category], abs(x.rank_gap)))
    
    # 6. Limit Output
    top_results = results[:5]

    return PredictResponse(
        rank=request.rank,
        category=request.category,
        college_type=request.college_type,
        total_results=len(results),
        results=top_results,
    )
