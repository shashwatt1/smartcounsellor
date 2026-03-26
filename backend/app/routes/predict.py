from fastapi import APIRouter, HTTPException
from app.models.schema import PredictRequest, PredictResponse
from app.services.predictor import predict_colleges

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest) -> PredictResponse:
    """
    Predict eligible colleges based on JEE rank and filters.

    **Quota Logic:**
    - IIT / IIIT → always AI quota
    - NIT → HS if home state matches institute state, else OS

    **Priority order (when college_type = ALL):**
    1. IIT
    2. NIT (HS first, then OS)
    3. IIIT
    """
    try:
        return predict_colleges(request)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc
