import pandas as pd
import streamlit as st
from supabase import create_client
from streamlit.errors import StreamlitSecretNotFoundError


st.set_page_config(page_title="Salary Prediction Dashboard", layout="wide")


def get_supabase_setting(name: str, fallback: str) -> str:
    try:
        return st.secrets[name]
    except (StreamlitSecretNotFoundError, KeyError):
        return fallback


SUPABASE_URL = get_supabase_setting(
    "SUPABASE_URL", "https://fezfntwxebavbchpfhqm.supabase.co"
)
SUPABASE_KEY = get_supabase_setting(
    "SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZlemZudHd4ZWJhdmJjaHBmaHFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2NDYwNTMsImV4cCI6MjA5MTIyMjA1M30.Kz9oVDlfkdrqrryUpeObAwzK4r5W4GNyINOSkeMUeU4",
)

PREDICTION_TABLE = "salary_predictions"
ANALYSIS_TABLE = "analysis_reports"


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


@st.cache_data(ttl=300)
def load_dashboard_data():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return pd.DataFrame(), {}, "Supabase credentials are not configured."

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        prediction_result = supabase.table(PREDICTION_TABLE).select("*").execute()
        analysis_result = (
            supabase.table(ANALYSIS_TABLE)
            .select("*")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        return pd.DataFrame(), {}, str(exc)

    prediction_rows = prediction_result.data or []
    analysis_rows = analysis_result.data or []

    predictions_df = pd.DataFrame(prediction_rows)
    latest_report = analysis_rows[0] if analysis_rows else {}
    return predictions_df, latest_report, None


def build_grouped_salary_chart(df: pd.DataFrame, group_col: str):
    required_cols = {group_col, "predicted_salary_in_usd"}
    if not required_cols.issubset(df.columns):
        return None

    chart_df = (
        df.groupby(group_col, dropna=False)["predicted_salary_in_usd"]
        .mean()
        .sort_values(ascending=False)
    )
    return chart_df if not chart_df.empty else None


st.title("Salary Prediction Dashboard")
st.caption(
    "Predictions, LLM analysis, and visualizations loaded from Supabase."
)

predictions_df, latest_report, load_error = load_dashboard_data()

if load_error:
    st.warning("Supabase data is temporarily unavailable.")
    st.caption(load_error)

if predictions_df.empty:
    st.info("No prediction data is available in Supabase yet.")
else:
    st.sidebar.header("Filters")

    filtered_df = predictions_df.copy()

    if "experience_level" in predictions_df.columns:
        experience_options = sorted(predictions_df["experience_level"].dropna().unique().tolist())
        selected_experience = st.sidebar.multiselect(
            "Experience Level", experience_options, default=experience_options
        )
        if selected_experience:
            filtered_df = filtered_df[filtered_df["experience_level"].isin(selected_experience)]

    if "job_title" in predictions_df.columns:
        job_options = sorted(predictions_df["job_title"].dropna().unique().tolist())
        selected_jobs = st.sidebar.multiselect("Job Title", job_options, default=job_options)
        if selected_jobs:
            filtered_df = filtered_df[filtered_df["job_title"].isin(selected_jobs)]

    if "company_size" in predictions_df.columns:
        size_options = sorted(predictions_df["company_size"].dropna().unique().tolist())
        selected_sizes = st.sidebar.multiselect("Company Size", size_options, default=size_options)
        if selected_sizes:
            filtered_df = filtered_df[filtered_df["company_size"].isin(selected_sizes)]

    st.subheader("Prediction Overview")

    if filtered_df.empty:
        st.info("No prediction rows match the current filters.")
    else:
        metric_cols = st.columns(4)
        metric_cols[0].metric("Rows", len(filtered_df))

        if "predicted_salary_in_usd" in filtered_df.columns:
            salary_series = pd.to_numeric(
                filtered_df["predicted_salary_in_usd"], errors="coerce"
            ).dropna()
        else:
            salary_series = pd.Series(dtype="float64")

        if salary_series.empty:
            metric_cols[1].metric("Average Salary", "N/A")
            metric_cols[2].metric("Highest Salary", "N/A")
            metric_cols[3].metric("Lowest Salary", "N/A")
        else:
            metric_cols[1].metric("Average Salary", format_currency(salary_series.mean()))
            metric_cols[2].metric("Highest Salary", format_currency(salary_series.max()))
            metric_cols[3].metric("Lowest Salary", format_currency(salary_series.min()))

        st.subheader("Visualizations")

        exp_chart = build_grouped_salary_chart(filtered_df, "experience_level")
        if exp_chart is not None:
            st.markdown("Average Salary by Experience Level")
            st.bar_chart(exp_chart)

        job_chart = build_grouped_salary_chart(filtered_df, "job_title")
        if job_chart is not None:
            st.markdown("Average Salary by Job Title")
            st.bar_chart(job_chart)

        remote_chart = build_grouped_salary_chart(filtered_df, "remote_ratio")
        if remote_chart is not None:
            st.markdown("Average Salary by Remote Ratio")
            st.bar_chart(remote_chart)

        with st.expander("Prediction Table"):
            st.dataframe(filtered_df, use_container_width=True)

st.subheader("LLM Analysis")

if not latest_report:
    st.info("No LLM analysis is available in Supabase yet.")
else:
    summary_text = latest_report.get("summary_text")
    llm_analysis = latest_report.get("llm_analysis")

    if summary_text:
        st.markdown("Summary")
        st.write(summary_text)

    if llm_analysis:
        st.markdown("Detailed Analysis")
        st.write(llm_analysis)

    if not summary_text and not llm_analysis:
        st.info("The latest analysis record exists, but its text fields are empty.")
