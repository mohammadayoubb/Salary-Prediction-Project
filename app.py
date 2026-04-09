import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from pathlib import Path
from supabase import create_client

# Supabase credentials
SUPABASE_URL = "https://fezfntwxebavbchpfhqm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZlemZudHd4ZWJhdmJjaHBmaHFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2NDYwNTMsImV4cCI6MjA5MTIyMjA1M30.Kz9oVDlfkdrqrryUpeObAwzK4r5W4GNyINOSkeMUeU4"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI endpoint
FASTAPI_URL = "https://salary-prediction-project-hru9.onrender.com/predict"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(page_title="Salary Prediction Dashboard", layout="wide")

st.title("Salary Prediction Dashboard")
st.write("This dashboard displays salary predictions and AI-generated analysis based on job-related input scenarios.")


job_titles_df = pd.read_csv(DATA_DIR / "cleaned_ds_salaries.csv")
job_title_options = sorted(job_titles_df["job_title"].dropna().unique().tolist())


# Interactive prediction form

st.subheader("Try a New Salary Prediction")

with st.form("prediction_form"):
    work_year = st.number_input("Work Year", min_value=2020, max_value=2030, value=2023)
    experience_level = st.selectbox("Experience Level", ["EN", "MI", "SE", "EX"])
    employment_type = st.selectbox("Employment Type", ["FT", "PT", "CT", "FL"])
    job_title = st.selectbox("Job Title", job_title_options)
    employee_residence = st.text_input("Employee Residence (2-letter country code)", value="US")
    remote_ratio = st.selectbox("Remote Ratio", [0, 50, 100])
    company_location = st.text_input("Company Location (2-letter country code)", value="US")
    company_size = st.selectbox("Company Size", ["S", "M", "L"])

    submitted = st.form_submit_button("Predict Salary")

if submitted:
    params = {
        "work_year": work_year,
        "experience_level": experience_level,
        "employment_type": employment_type,
        "job_title": job_title,
        "employee_residence": employee_residence.upper(),
        "remote_ratio": remote_ratio,
        "company_location": company_location.upper(),
        "company_size": company_size
    }

    try:
        response = requests.get(FASTAPI_URL, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()

        if "predicted_salary_in_usd" in result:
            st.success(f"Predicted Salary: ${result['predicted_salary_in_usd']:,.2f}")
        else:
            st.error(f"Unexpected API response: {result}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error calling prediction API: {e}")


# aam njeeb il data min supabase

pred_response = supabase.table("salary_predictions").select("*").execute()
pred_data = pred_response.data

analysis_response = supabase.table("analysis_reports").select("*").order("created_at", desc=True).limit(1).execute()
analysis_data = analysis_response.data


# Predictions section

if not pred_data:
    st.warning("No prediction data found in Supabase.")
else:
    df = pd.DataFrame(pred_data)

    st.subheader("Prediction Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Predictions", len(df))
    col2.metric("Average Salary", f"${df['predicted_salary_in_usd'].mean():,.2f}")
    col3.metric("Highest Salary", f"${df['predicted_salary_in_usd'].max():,.2f}")
    col4.metric("Lowest Salary", f"${df['predicted_salary_in_usd'].min():,.2f}")

    st.subheader("Prediction Table")
    st.dataframe(df)

    st.subheader("Average Predicted Salary by Experience Level")
    avg_salary_by_exp = df.groupby("experience_level")["predicted_salary_in_usd"].mean().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    avg_salary_by_exp.plot(kind="bar", ax=ax)
    ax.set_title("Average Predicted Salary by Experience Level")
    ax.set_xlabel("Experience Level")
    ax.set_ylabel("Predicted Salary in USD")
    ax.tick_params(axis="x", rotation=0)

    st.pyplot(fig)


# LLM 

st.subheader("LLM Analysis")

if not analysis_data:
    st.warning("No analysis report found in Supabase.")
else:
    latest_report = analysis_data[0]
    st.write(latest_report["llm_analysis"])


#hayda il part optional lal summary
   # with st.expander("Show Summary Text"):
    #    st.write(latest_report["summary_text"])
