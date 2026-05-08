# API routes related to transaction analysis
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.csv_parser import parse_csv
from app.services.timeline_service import generate_monthly_timeline
from app.services.stress_detector import detect_stress_indicators
from app.services.scoring_service import calculate_stress_score
from app.services.recommendation_service import generate_forward_view
from app.models.response_models import AnalysisResponse

# Create API router
router = APIRouter(tags=["Cashflow Analysis"])

@router.post(
        "/analyse",
        response_model=AnalysisResponse,
        response_model_exclude_none=True
)
async def analyse_cashflow(
    file: UploadFile = File(...)
):
    # Analyse upload csv transaction file and return stress analysis.

    # Validate uploaded file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )
    try:
        # Parse and clean uploaded CSV
        transactions_df = await parse_csv(file)

        # Generate monthly cashflow timeline
        monthly_timeline = generate_monthly_timeline(transactions_df)

        # Detect financial stress indicators
        stress_indicators = detect_stress_indicators(transactions_df, monthly_timeline)

        # Calculate deterministic stress score
        score_result = calculate_stress_score(stress_indicators)

        # Generate forward risk assessment
        forward_view = generate_forward_view(score_result["final_score"], stress_indicators)

        # Return temporary response for testing
        return {
            "message": "CSV processed successfully ",
            "total_transactions": len(transactions_df),
            "monthly_timeline": monthly_timeline,
            "stress_indicators": stress_indicators,
            "stress_score": score_result,
            "forward_view": forward_view
        }
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(error)}"
        )
    