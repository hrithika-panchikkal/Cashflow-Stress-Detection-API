# API routes related to transaction analysis
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.csv_parser import parse_csv
from app.services.timeline_service import generate_monthly_timeline

# Create API router
router = APIRouter()

@router.post("/analyse")
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

        # Return temporary response for testing
        return {
            "message": "CSV processed successfully ",
            "total_transactions": len(transactions_df),
            "monthly_timeline": monthly_timeline
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
    