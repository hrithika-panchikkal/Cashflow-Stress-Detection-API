# FastAPI application entry point

from fastapi import FastAPI
from app.api.analyse import router as analyse_router

# Create FastAPI app instance

app = FastAPI(
    title="Cashflow Stress Detection API",
    description="API for detecting financial stress signals from bank transaction CSVs",
    version="1.0.0"
)

# Health check endpoint

@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "Cashflow Stress Detection API is running"
    }
# Register analyse routes
app.include_router(analyse_router)