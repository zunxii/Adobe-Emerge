import pandas as pd
import json

# Load NLP-to-SQL dataset
with open("../datasets/nlp_to_sql.json", "r") as file:
    nlp_to_sql_data = json.load(file)

# Load Incorrect-to-Correct SQL dataset
with open("../datasets/sql_correction.json", "r") as file:
    sql_correction_data = json.load(file)

# Convert to Pandas DataFrames
df_nlp_to_sql = pd.DataFrame(nlp_to_sql_data)
df_sql_correction = pd.DataFrame(sql_correction_data)

print("NLP-to-SQL Dataset Sample:\n", df_nlp_to_sql.head())
print("SQL Correction Dataset Sample:\n", df_sql_correction.head())
