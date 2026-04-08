import pandas as pd
import matplotlib.pyplot as plt

# Load prediction results
df = pd.read_csv(r"C:\Users\user\Downloads\se factory Project\prediction_results.csv")

# Average salary by experience level
avg_salary_by_exp = df.groupby("experience_level")["predicted_salary_in_usd"].mean().sort_index()

print(avg_salary_by_exp)

# Plot chart
plt.figure(figsize=(8, 5))
avg_salary_by_exp.plot(kind="bar")
plt.title("Average Predicted Salary by Experience Level")
plt.xlabel("Experience Level")
plt.ylabel("Predicted Salary in USD")
plt.xticks(rotation=0)
plt.tight_layout()

# Save chart
plt.savefig("salary_by_experience.png")
plt.show()

print("Chart saved as salary_by_experience.png")

# Summary tables
avg_salary_by_title = df.groupby("job_title")["predicted_salary_in_usd"].mean().sort_values(ascending=False)
avg_salary_by_remote = df.groupby("remote_ratio")["predicted_salary_in_usd"].mean().sort_index()
avg_salary_by_company_size = df.groupby("company_size")["predicted_salary_in_usd"].mean().sort_index()

summary_text = f"""
Summary of prediction results:

1. Average predicted salary by experience level:
{avg_salary_by_exp.to_string()}

2. Average predicted salary by job title:
{avg_salary_by_title.to_string()}

3. Average predicted salary by remote ratio:
{avg_salary_by_remote.to_string()}

4. Average predicted salary by company size:
{avg_salary_by_company_size.to_string()}
"""

print(summary_text)
with open("summary_text.txt", "w", encoding="utf-8") as f:
    f.write(summary_text)

print("Summary saved as summary_text.txt")

import ollama

prompt = f"""
You are a professional data analyst.

I have a salary prediction dataset produced by a machine learning model.
Based on the summary below, write a clear narrative analysis of the salary landscape.

Requirements:
- Explain the main salary patterns.
- Highlight how experience level affects salary.
- Mention differences across job titles.
- Comment on remote ratio and company size if relevant.
- Write in a professional but clear style.
- Make the explanation insightful, not generic filler.
- Refer to the chart titled 'Average Predicted Salary by Experience Level'.

Here is the summary:
{summary_text}
"""

response = ollama.chat(
    model="qwen2.5:0.5b",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

analysis_text = response["message"]["content"]

print("\nLLM Analysis:\n")
print(analysis_text)

with open("llm_analysis.txt", "w", encoding="utf-8") as f:
    f.write(analysis_text)

print("LLM analysis saved as llm_analysis.txt")