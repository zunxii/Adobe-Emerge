import pandas as pd
import json
import os

# Correct file paths
dataset_dir = os.path.join(os.getcwd(), "datasets")

# Load the NLP-to-SQL dataset
with open(os.path.join(dataset_dir, "nlp_to_sql.json"), "r") as file:
    nlp_to_sql_data = json.load(file)

# Load the incorrect-to-correct SQL dataset
with open(os.path.join(dataset_dir, "sql_correction.json"), "r") as file:
    sql_correction_data = json.load(file)

# Convert to DataFrame for easy handling
df_nlp_to_sql = pd.DataFrame(nlp_to_sql_data)
df_sql_correction = pd.DataFrame(sql_correction_data)

print(df_nlp_to_sql.head())  # Check first few rows
print(df_sql_correction.head())
