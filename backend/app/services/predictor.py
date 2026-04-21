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

def get_branch_priority(branch_name: str) -> int:
    name_lower = branch_name.lower()
    if "computer science" in name_lower or "cse" in name_lower:
        return 1
    if any(kw in name_lower for kw in ["artificial intelligence", "ai", "data science", "machine learning", "information technology", "it"]):
        return 2
    if any(kw in name_lower for kw in ["electronics", "ece", "electrical"]):
        return 3
    if any(kw in name_lower for kw in ["mechanical", "civil", "chemical", "metallurgy", "production"]):
        return 4
    return 5

def predict_colleges(request: PredictRequest) -> PredictResponse:
    df = load_josaa_data()
    
    # 1. Base Integrity: Remove NaN closing ranks
    df = df.dropna(subset=['closing_rank'])
    
    # 2. Vectorized exact matches (Massively speeds up subsetting)
    cat_mask = df['seat_type'].str.strip().str.upper() == request.category.strip().upper()
    gender_mask = df['gender'].str.strip().str.lower() == request.gender.strip().lower()
    df = df[cat_mask & gender_mask].copy()

    # 3. Apply EXAM_TYPE filter
    df['calc_college_type'] = df['institute'].apply(lambda x: classify_institute(str(x)).value)
    if request.exam_type == "JEE_MAIN":
        df = df[df['calc_college_type'] != "IIT"]
    elif request.exam_type == "JEE_ADVANCED":
        df = df[df['calc_college_type'] == "IIT"]

    # 4. Compute rank_gap and Apply deterministic margin filter
    df['closing_rank'] = df['closing_rank'].astype(int)
    margin = 1000
    df = df[(df['closing_rank'] >= request.rank - margin) & (df['closing_rank'] <= request.rank + margin)].copy()
    
    # Symmetric rank gap
    df['rank_gap'] = (df['closing_rank'] - request.rank).abs()

    # Stop early if empty
    if df.empty:
        return PredictResponse(rank=request.rank, category=request.category, college_type=request.college_type, total_results=0, results=[])

    # 5. Apply custom python logic logic on the deeply filtered subset
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
        closing = int(row['closing_rank'])
        if closing >= request.rank:
            chance = "Safe"
        elif gap < 500:
            chance = "Moderate"
        else:
            chance = "Dream"

        opening = row.get("opening_rank", 0)
        branch = extract_branch_name(program_name)
        
        results.append(CollegeResult(
            institute=institute,
            program=program_name,
            branch=branch,
            program_type=get_program_type(program_name),
            college_type=ctype.value,
            quota=row_quota,
            seat_type=str(row['seat_type']).strip().upper(),
            gender=str(row['gender']).strip(),
            opening_rank=int(opening) if not pd.isna(opening) else 0,
            closing_rank=closing,
            rank_gap=gap,
            chance_category=chance,
            branch_priority=get_branch_priority(branch),
            priority=_PRIORITY.get(ctype, 5)
        ))

    # 6. Sorting & Extraction logic based on exam type
    if request.exam_type == "JEE_MAIN":
        # Safe Options
        safe_results = [r for r in results if r.closing_rank >= request.rank]
        safe_results.sort(key=lambda x: (x.rank_gap, x.branch_priority))
        top_safe = safe_results[:2]
        
        # HS Options (NIT ONLY)
        hs_results = [r for r in results if r.quota == "HS" and r.college_type == "NIT"]
        hs_results.sort(key=lambda x: (x.rank_gap, x.branch_priority))
        top_hs = hs_results[:2]
        
        # Remaining results
        used_ids = {id(r) for r in top_safe + top_hs}
        remaining = [r for r in results if id(r) not in used_ids]
        remaining.sort(key=lambda x: (x.rank_gap, x.branch_priority))
        
        remaining_needed = 5 - len(top_safe) - len(top_hs)
        top_remaining = remaining[:remaining_needed] if remaining_needed > 0 else []
        
        # Combine
        top_results = top_hs + top_safe + top_remaining
        top_results = top_results[:5]
        
    else:
        # JEE_ADVANCED flow
        # Safe Options
        safe_results = [r for r in results if r.closing_rank >= request.rank]
        safe_results.sort(key=lambda x: (x.rank_gap, x.branch_priority))
        
        # Remaining results
        used_ids = {id(r) for r in safe_results}
        remaining = [r for r in results if id(r) not in used_ids]
        remaining.sort(key=lambda x: (x.rank_gap, x.branch_priority))
        
        # Combine blindly without HS logic
        top_results = safe_results + remaining
        top_results = top_results[:5]

    return PredictResponse(
        rank=request.rank,
        category=request.category,
        college_type=request.college_type,
        total_results=len(results),
        results=top_results,
    )
