import requests
import pandas as pd
from itertools import product

url = "http://127.0.0.1:8000/predict"

# Representative values
work_years = [2022, 2023]
experience_levels = ["EN", "MI", "SE", "EX"]
employment_types = ["FT"]
job_titles = ["Data Scientist", "Data Engineer", "Machine Learning Engineer"]
employee_residences = ["US"]
remote_ratios = [0, 50, 100]
company_locations = ["US"]
company_sizes = ["S", "M", "L"]

results = []

combinations = product(
    work_years,
    experience_levels,
    employment_types,
    job_titles,
    employee_residences,
    remote_ratios,
    company_locations,
    company_sizes
)

for combo in combinations:
    params = {
        "work_year": combo[0],
        "experience_level": combo[1],
        "employment_type": combo[2],
        "job_title": combo[3],
        "employee_residence": combo[4],
        "remote_ratio": combo[5],
        "company_location": combo[6],
        "company_size": combo[7]
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        prediction = response.json().get("predicted_salary_in_usd")

        results.append({
            **params,
            "predicted_salary_in_usd": prediction
        })

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {params}: {e}")

# Convert results to DataFrame
results_df = pd.DataFrame(results)

print(results_df.head())
print("Total successful predictions:", len(results_df))

# Save results
results_df.to_csv("prediction_results.csv", index=False)
print("Saved as prediction_results.csv")