from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
import torch
import pandas as pd
import json

# Load dataset
with open("../datasets/nlp_to_sql.json", "r") as file:
    nlp_to_sql_data = json.load(file)

train_data = [(row["nlp"], row["sql"]) for row in nlp_to_sql_data]

# Load tokenizer and model
model_name = "t5-small"  # Try "t5-base" for better results
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Prepare training data
train_texts = [f"translate English to SQL: {nlp}" for nlp, sql in train_data]
train_labels = [sql for _, sql in train_data]

train_encodings = tokenizer(train_texts, padding=True, truncation=True, return_tensors="pt")
label_encodings = tokenizer(train_labels, padding=True, truncation=True, return_tensors="pt")

class SQLDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}, \
               torch.tensor(self.labels["input_ids"][idx])

    def __len__(self):
        return len(self.labels["input_ids"])

train_dataset = SQLDataset(train_encodings, label_encodings)

training_args = TrainingArguments(
    output_dir="../models/sql_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()
model.save_pretrained("../models/sql_model")
tokenizer.save_pretrained("../models/sql_model")
