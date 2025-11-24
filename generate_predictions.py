import pandas as pd
import numpy as np
from main import get_openai_embedding
import faiss

df = pd.read_csv("data/shl_with_embeddings.csv")
df["openai_embedding"] = df["openai_embedding"].apply(eval)
embedding_matrix = np.vstack(df["openai_embedding"].values).astype("float32")
faiss.normalize_L2(embedding_matrix)
index = faiss.IndexFlatIP(embedding_matrix.shape[1])
index.add(embedding_matrix)

def get_recommendations(query: str, top_k: int = 10, threshold: float = 0.35):
    query_vec = get_openai_embedding(query)
    faiss.normalize_L2(query_vec)
    
    scores, indices = index.search(query_vec, min(top_k * 2, 50))
    
    recommendations = []
    for score, idx in zip(scores[0], indices[0]):
        if score >= threshold and len(recommendations) < top_k:
            recommendations.append(df.iloc[idx]["url"])
    
    if len(recommendations) < 5:
        for score, idx in zip(scores[0], indices[0]):
            if len(recommendations) >= top_k:
                break
            url = df.iloc[idx]["url"]
            if url not in recommendations:
                recommendations.append(url)
    
    return recommendations[:top_k]

def generate_test_predictions(test_file: str, output_file: str = "predictions.csv"):
    test_df = pd.read_csv(test_file)
    
    query_col = "Query" if "Query" in test_df.columns else "query"
    
    predictions = []
    
    for idx, row in test_df.iterrows():
        query = row[query_col]
        recommended_urls = get_recommendations(query, top_k=10)
        
        for url in recommended_urls:
            predictions.append({
                "query": query,
                "Assessment_url": url
            })
    
    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv(output_file, index=False)
    
    return predictions_df

if __name__ == "__main__":
    test_file = "data/test_data.csv"
    output_file = "output/predictions.csv"
    
    predictions_df = generate_test_predictions(test_file, output_file)
    print(f"Predictions saved to {output_file}")
