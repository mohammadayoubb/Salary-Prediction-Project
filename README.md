
# Salary Prediction Project

This project predicts data science salaries based on job-related information such as experience level, employment type, job title, company size, location, and remote ratio.

It was built as a Week 1 AI bootcamp assignment and includes the full pipeline from data cleaning to deployment.

## What the project does

The project takes job details as input and predicts the salary in USD using a trained Decision Tree model.

It also includes:
- a FastAPI endpoint for predictions
- a Python script that calls the API
- a local LLM analysis step using Ollama
- Supabase for storing results
- a Streamlit dashboard for displaying predictions and analysis

## Main steps

1. Cleaned the dataset  
2. Trained a Decision Tree regression model  
3. Saved the trained model  
4. Built a FastAPI GET endpoint for prediction  
5. Created a Python script to call the API on multiple input combinations  
6. Generated analysis and a chart using a local LLM with Ollama  
7. Stored predictions and analysis in Supabase  
8. Built a Streamlit dashboard connected to Supabase  
9. Deployed the FastAPI app and the Streamlit dashboard  

## Tools used

- Python
- Pandas
- Scikit-learn
- FastAPI
- Uvicorn
- Requests
- Matplotlib
- Ollama
- Supabase
- Streamlit

## Dataset

The dataset used is the Data Science Job Salaries dataset from Kaggle.

Target column y:
  salary_in_usd

    Main input features x:
    work_year
    experience_level
    employment_type
    job_title
    employee_residence
    remote_ratio
    company_location
    company_size

## Model

The model used in this project is:

- RandomForestRegressor

The trained model is saved as a `.pkl` file and then loaded by the FastAPI app for prediction.

## API

The FastAPI app provides:

- `GET /` → checks that the API is running
- `GET /predict` → returns the predicted salary based on the input fields

Example input fields:
- work year
- experience level
- employment type
- job title
- employee residence
- remote ratio
- company location
- company size

## Dashboard

The Streamlit dashboard shows:
- salary prediction overview
- prediction table
- chart of average predicted salary by experience level
- LLM-generated analysis
- form for trying a new prediction manually

## Supabase

Supabase is used to store:
- prediction records
- analysis results

This allows the dashboard to read data directly from the database instead of relying on local files.

