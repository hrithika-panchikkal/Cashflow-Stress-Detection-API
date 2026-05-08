# API routes related to transaction analysis

from fastapi import APIRouter, UploadFile, File

# Create API router

router = APIRouter()

@router.post("/analyse")
async def analyse_cashflow(
    file: UploadFile = File(...)
):
    # Analyse upload csv transaction file and return stress analysis.
    return {
        "filename": file.filename,
        "message": "File received successfully"
    }
    