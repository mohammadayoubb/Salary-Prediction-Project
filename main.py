from fastapi import FastAPI, Query
import pandas as pd
import joblib
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FASTAPI_URL = os.getenv("FASTAPI_URL")

# Create FastAPI app
app = FastAPI(title="Salary Prediction API")

# Load trained model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "improved_salary_prediction_model.pkl"
model = joblib.load(MODEL_PATH)
# Allowed values for validation
ALLOWED_EXPERIENCE_LEVELS = ["EN", "MI", "SE", "EX"]
ALLOWED_EMPLOYMENT_TYPES = ["FT", "PT", "CT", "FL"]
ALLOWED_REMOTE_RATIOS = [0, 50, 100]
ALLOWED_COMPANY_SIZES = ["S", "M", "L"]

@app.get("/")
def home():
    return {"message": "Salary Prediction API is running"}

@app.get("/predict")
def predict_salary(
    work_year: int = Query(..., ge=2020, le=2030),
    experience_level: str = Query(...),
    employment_type: str = Query(...),
    job_title: str = Query(...),
    employee_residence: str = Query(..., min_length=2, max_length=2),
    remote_ratio: int = Query(...),
    company_location: str = Query(..., min_length=2, max_length=2),
    company_size: str = Query(...)
):
    # Manual validation
    if experience_level not in ALLOWED_EXPERIENCE_LEVELS:
        return {"error": f"experience_level must be one of {ALLOWED_EXPERIENCE_LEVELS}"}

    if employment_type not in ALLOWED_EMPLOYMENT_TYPES:
        return {"error": f"employment_type must be one of {ALLOWED_EMPLOYMENT_TYPES}"}

    if remote_ratio not in ALLOWED_REMOTE_RATIOS:
        return {"error": f"remote_ratio must be one of {ALLOWED_REMOTE_RATIOS}"}

    if company_size not in ALLOWED_COMPANY_SIZES:
        return {"error": f"company_size must be one of {ALLOWED_COMPANY_SIZES}"}

    
    input_data = pd.DataFrame([{
        "work_year": work_year,
        "experience_level": experience_level,
        "employment_type": employment_type,
        "job_title": job_title,
        "employee_residence": employee_residence,
        "remote_ratio": remote_ratio,
        "company_location": company_location,
        "company_size": company_size
    }])

    # Predict
    prediction = model.predict(input_data)[0]

    return {
        "predicted_salary_in_usd": round(float(prediction), 2)
    }
