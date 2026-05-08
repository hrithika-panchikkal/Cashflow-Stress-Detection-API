# Cashflow Stress Detection API

A production-style FastAPI backend service that analyzes bank transaction CSVs to detect financial stress signals and generate deterministic lending risk assessments.

The system processes real-world noisy transaction data, computes monthly cashflow analytics, detects financial stress indicators, calculates a rule-based stress score, and returns a forward-looking risk recommendation.

---

# Features

- CSV transaction ingestion via REST API
- Monthly cashflow timeline generation
- Financial stress signal detection
- Deterministic 0–100 stress scoring
- Lending risk recommendation engine
- Graceful malformed-row handling
- Typed API responses using Pydantic
- Swagger/OpenAPI documentation
- Unit tests for scoring and API validation

---

# Tech Stack

- Python
- FastAPI
- Pandas
- Pydantic
- Pytest

---

# Project Structure

```text
app/
├── api/
├── services/
├── models/
├── utils/
├── config/
└── main.py

tests/
├── test_api.py
└── test_scoring.py
```

---

# API Endpoint

## Analyse Transactions

```http
POST /analyse
```

Accepts:
- CSV file upload

Returns:
- monthly_timeline
- stress_indicators
- stress_score
- forward_view

---

# Expected CSV Columns

| Column | Description |
|---|---|
| date | Transaction date |
| description | Transaction description |
| amount | Transaction amount |
| balance_after | Account balance after transaction |
| type | credit/debit |

---

# Detected Stress Indicators

The system detects the following financial stress signals:

- Bounced/returned payments
- Negative cashflow months
- Delayed salary payments (>7 days)
- Sustained low-balance periods
- Revenue decline trends

---

# Stress Score Methodology

Stress score is deterministic and rule-based.

Score range:

| Score | Meaning |
|---|---|
| 0 | No financial stress |
| 100 | Severe financial stress / decline |

The score is calculated using weighted additions from detected stress indicators.

## Scoring Weights

| Indicator | Scoring Logic |
|---|---|
| bounced_payments | count × 3 |
| negative_cashflow | months × 6 |
| low_balance_period | +10 |
| delayed_salary_payments | months × 2 |
| revenue_decline | +8 |

Final score is capped at 100.

---

# Risk Classification

| Score Range | Risk Level |
|---|---|
| 0–20 | low_risk |
| 21–50 | moderate_risk |
| 51–80 | high_risk |
| 81–100 | decline |

---

# Malformed Row Handling

The system gracefully handles malformed transaction rows using:
- safe datetime parsing
- numeric coercion
- null filtering
- validation checks

Invalid rows are skipped without terminating processing.

---

# Multi-Currency Readiness

The architecture is designed to support future multi-currency enhancements through dedicated service abstraction and modular transaction processing.

---

# Running The Application

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start Server

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Running Tests

```bash
pytest
```

---

# Future Improvements

- Consecutive low-balance day tracking
- Historical payroll cycle modeling
- Multi-currency normalization
- Database persistence
- Authentication and authorization
- Advanced anomaly detection

---

# Notes

This project intentionally uses deterministic financial heuristics and avoids LLM/AI-based scoring in order to maintain explainability, reproducibility, and predictable decisioning behavior.