from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load trained model
model_name = "../models/sql_model"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_sql(nlp_query):
    input_text = "translate English to SQL: " + nlp_query
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids)
    generated_sql = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_sql

# Example
nlp_query = "Show all employees"
print("Generated SQL:", generate_sql(nlp_query))
