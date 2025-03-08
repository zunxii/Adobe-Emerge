import requests
import json
import os

# Load Groq API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ ERROR: GROQ_API_KEY is not set! Set it in your environment variables.")

# Base URL for Groq API
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Define model (Use valid Groq model)
MODEL = "llama3-70b-8192"  # Valid models: mixtral-8x7b, llama3-8b-8192, llama3-70b-8192

# Load datasets safely
DATASET_PATHS = {
    "nlp_to_sql": "datasets/nlp_to_sql.json",
    "sql_correction": "datasets/sql_correction.json"
}

datasets = {}

for key, path in DATASET_PATHS.items():
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ ERROR: {path} not found! Ensure the datasets exist in the correct directory.")
    with open(path, "r", encoding="utf-8") as file:
        datasets[key] = json.load(file)

# Store results
results = {
    "nlp_to_sql": [],
    "sql_correction": []
}


def send_request(messages, model=MODEL):
    """ Sends a request to the Groq API """
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.0,
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        # Extract response safely
        if "choices" in result and result["choices"]:
            return result["choices"][0].get("message", {}).get("content", None)
        else:
            print("⚠️ Unexpected API Response:", result)
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Failed: {e}")
        return None


def train_nlp_to_sql():
    """ Train AI model to generate SQL from natural language """
    print("\n🔄 Training NLP-to-SQL model...\n")

    for entry in datasets["nlp_to_sql"]:
        nl_query = entry.get("NL")
        expected_sql = entry.get("Query")

        if not nl_query or not expected_sql:
            print("⚠️ Skipping invalid entry:", entry)
            continue

        messages = [
            {"role": "system", "content": "Convert natural language into SQL queries."},
            {"role": "user", "content": f"Convert this to SQL: {nl_query}"}
        ]

        generated_sql = send_request(messages)
        if generated_sql:
            print(f"📝 NL Query: {nl_query}")
            print(f"🛠️ Generated SQL: {generated_sql}")
            print(f"✅ Expected SQL: {expected_sql}\n")

            # Save result
            results["nlp_to_sql"].append({
                "NL": nl_query,
                "Generated_SQL": generated_sql,
                "Expected_SQL": expected_sql
            })
        else:
            print(f"❌ Failed to generate SQL for: {nl_query}\n")


def train_sql_correction():
    """ Train AI model to correct SQL syntax errors """
    print("\n🔄 Training SQL Correction model...\n")

    for entry in datasets["sql_correction"]:
        incorrect_sql = entry.get("incorrect_sql")
        correct_sql = entry.get("correct_sql")

        if not incorrect_sql or not correct_sql:
            print("⚠️ Skipping invalid entry:", entry)
            continue

        messages = [
            {"role": "system", "content": "Fix errors in SQL queries."},
            {"role": "user", "content": f"Fix this SQL: {incorrect_sql}"}
        ]

        corrected_sql = send_request(messages)
        if corrected_sql:
            print(f"❌ Incorrect SQL: {incorrect_sql}")
            print(f"🛠️ Corrected SQL: {corrected_sql}")
            print(f"✅ Expected SQL: {correct_sql}\n")

            # Save result
            results["sql_correction"].append({
                "Incorrect_SQL": incorrect_sql,
                "Corrected_SQL": corrected_sql,
                "Expected_SQL": correct_sql
            })
        else:
            print(f"❌ Failed to correct SQL: {incorrect_sql}\n")


def export_results():
    """ Export results to a JSON file """
    output_path = "datasets/training_results.json"

    # Ensure the "datasets" folder exists
    os.makedirs("datasets", exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4, ensure_ascii=False)
        print(f"\n📁 Results successfully exported to {output_path}")
    except Exception as e:
        print(f"❌ Error writing JSON file: {e}")


if __name__ == "__main__":
    train_nlp_to_sql()
    train_sql_correction()
    export_results()
    print("\n✅ Training completed!")
