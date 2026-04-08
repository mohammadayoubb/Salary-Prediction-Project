import pandas as pd
from pathlib import Path
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://fezfntwxebavbchpfhqm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZlemZudHd4ZWJhdmJjaHBmaHFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2NDYwNTMsImV4cCI6MjA5MTIyMjA1M30.Kz9oVDlfkdrqrryUpeObAwzK4r5W4GNyINOSkeMUeU4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "requirements.txt").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Load predictions CSV
df = pd.read_csv(DATA_DIR / "prediction_results.csv")

# Convert dataframe to list of dictionaries
prediction_records = df.to_dict(orient="records")

# Insert into salary_predictions table
response = supabase.table("salary_predictions").insert(
    prediction_records,
    returning="representation"
).execute()

print("Prediction results uploaded successfully.")
print(response)

##########################################################################

# Read saved summary and LLM analysis
with open(DATA_DIR / "summary_text.txt", "r", encoding="utf-8") as f:
    summary_text = f.read()

with open(DATA_DIR / "llm_analysis.txt", "r", encoding="utf-8") as f:
    llm_analysis = f.read()

analysis_record = {
    "summary_text": summary_text,
    "llm_analysis": llm_analysis,
    "chart_filename": str(ASSETS_DIR / "salary_by_experience.png")
}

response = supabase.table("analysis_reports").insert(
    analysis_record,
    returning="representation"
).execute()

print("Analysis report uploaded successfully.")
print(response)
