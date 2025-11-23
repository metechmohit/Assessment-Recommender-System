import pandas as pd
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
df = pd.read_csv("data/shl_products_catalog.csv")

# Clean 'duration' column
numeric_durations_temp = df['duration'].str.extract(r'(\d+)').astype(float)
average_duration_scalar = numeric_durations_temp.mean().iloc[0]
df['duration'] = df['duration'].replace('N/A', np.nan)
df['duration'] = df['duration'].fillna(f"{int(average_duration_scalar)} min")
if 'duration_cleaned' in df.columns:
    df = df.drop(columns=['duration_cleaned'])

# Create the embedding text
df["embedding_text"] = (
    df["name"] + ". " +
    df["description"] + ". " +
    "Test Type: " + df["test_type"] + ". " +
    "Duration: " + df["duration"] + "long " +". " +
    "Remote Testing: " + df["remote_support"] + ". " +
    "Adaptive Support: " + df["adaptive_support"]
)

# Generate OpenAI embeddings
def get_openai_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

df["openai_embedding"] = df["embedding_text"].apply(get_openai_embedding)

# Save final version
df.to_csv("data/shl_with_embeddings.csv", index=False)
