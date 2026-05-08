from typing import List, Optional
from pydantic import BaseModel

# Monthly timeline model
class MonthlyTimeline(BaseModel):

    month: str
    total_inflows: float
    total_outflows: float
    net_flow: float
    end_balance: float

# Stress indicator model
class StressIndicator(BaseModel):

    type: str
    severity: str

    # Optional fields
    count: Optional[int] = None
    months: Optional[list] = None
    days: Optional[int] = None
    threshold: Optional[float] = None
    declining_months: Optional[int] = None
    class Config:
        exclude_none = True

# Score breakdown model
class ScoreBreakdown(BaseModel):

    indicator: str
    points: int

# Stress score model
class StressScore(BaseModel):

    final_score: int
    score_breakdown: List[ScoreBreakdown]

# Forward view model
class ForwardView(BaseModel):

    status: str
    reason: str

# Final API response model
class AnalysisResponse(BaseModel):

    message: str
    total_transactions: int

    monthly_timeline: List[
        MonthlyTimeline
    ]

    stress_indicators: List[
        StressIndicator
    ]

    stress_score: StressScore

    forward_view: ForwardView