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
    results: list[CollegeResult] = []

    for _, row in df.iterrows():
        result = _evaluate_row(row, request)
        if result is not None:
            results.append(result)

    # Sort priorities
    results.sort(key=lambda r: (r.priority, r.rank_gap))

    return PredictResponse(
        rank=request.rank,
        category=request.category,
        college_type=request.college_type,
        total_results=len(results),
        results=results[:TOP_N],
    )

def _evaluate_row(row: Any, req: PredictRequest) -> CollegeResult | None:
    institute: str = str(row.get("institute", ""))
    program_name: str = str(row.get("academic_program_name", ""))
    seat_type: str = str(row.get("seat_type", ""))
    gender: str = str(row.get("gender", ""))
    closing_rank = row.get("closing_rank", 0)
    opening_rank = row.get("opening_rank", 0)
    row_quota: str = str(row.get("quota", ""))
    
    # 1. Base Integrity Check
    if pd.isna(closing_rank):
        return None

    # 2. Category mismatch
    if seat_type.strip().upper() != req.category.strip().upper():
        return None

    # 3. Dynamic Rank Margin Check
    # Instead of strict cutoff, allows a margin of error for ambitious/safe colleges.
    # At lower ranks, limit is tight. At higher ranks, the absolute fluctuation can be larger.
    rank_gap = int(closing_rank) - req.rank
    margin = max(1000, int(req.rank * 0.15))
    
    # rank_gap < 0 means student rank is worse than closing (Ambitious)
    # rank_gap > 0 means student rank is better than closing (Safe)
    if rank_gap < -margin or rank_gap > (margin * 1.5):
        return None

    # 3. Gender mismatch
    # Data often uses "Gender-Neutral" vs frontend matching. Handle trailing spaces.
    if gender.strip().lower() != req.gender.strip().lower():
        return None

    # 4. Program type
    if not req.include_five_year and is_five_year_program(program_name):
        return None

    # 5. College type
    college_type = classify_institute(institute)
    if req.college_type != "ALL" and college_type.value != req.college_type:
        return None

    # 6. Quota logic (HS vs OS/AI)
    valid_quotas = get_quota_for_institute(institute, req.home_state)
    if row_quota.strip().upper() not in [q.upper() for q in valid_quotas]:
        return None

    # 7. Scoring
    rank_gap = int(closing_rank) - req.rank

    return CollegeResult(
        institute=institute,
        program=program_name,
        branch=extract_branch_name(program_name),
        program_type=get_program_type(program_name),
        college_type=college_type.value,
        quota=row_quota.strip().upper(),
        seat_type=seat_type.strip().upper(),
        gender=gender.strip(),
        opening_rank=int(opening_rank) if not pd.isna(opening_rank) else 0,
        closing_rank=int(closing_rank),
        rank_gap=rank_gap,
        priority=_PRIORITY.get(college_type, 5),
    )
