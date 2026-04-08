import pandas as pd
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://fezfntwxebavbchpfhqm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZlemZudHd4ZWJhdmJjaHBmaHFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2NDYwNTMsImV4cCI6MjA5MTIyMjA1M30.Kz9oVDlfkdrqrryUpeObAwzK4r5W4GNyINOSkeMUeU4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load predictions CSV
df = pd.read_csv(r"C:\Users\user\Downloads\se factory Project\prediction_results.csv")

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
with open(r"C:\Users\user\Downloads\se factory Project\summary_text.txt", "r", encoding="utf-8") as f:
    summary_text = f.read()

with open(r"C:\Users\user\Downloads\se factory Project\llm_analysis.txt", "r", encoding="utf-8") as f:
    llm_analysis = f.read()

analysis_record = {
    "summary_text": summary_text,
    "llm_analysis": llm_analysis,
    "chart_filename": r"C:\Users\user\Downloads\se factory Project\salary_by_experience.png"
}

response = supabase.table("analysis_reports").insert(
    analysis_record,
    returning="representation"
).execute()

print("Analysis report uploaded successfully.")
print(response)