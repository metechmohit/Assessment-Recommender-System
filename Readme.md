# SHL Assessment Recommendation System

A semantic search-powered recommendation engine for SHL assessments. Users can enter natural language queries (e.g., job descriptions, URLs containing JDs), and the system returns the most relevant individual assessments using OpenAI embeddings and FAISS similarity search — delivered via a FastAPI endpoint.

---

## Approach (In Brief)

1. **Scraping**: Collected structured data from SHL’s product catalog using `Selenium` and `BeautifulSoup`.
2. **Embedding Text Construction**: Combined assessment name, description, type, and support details for contextual embedding.
3. **Embedding Generation**: Used OpenAI’s `text-embedding-3-small` model to generate vector representations.
4. **Similarity Search**: Indexed vectors with FAISS and performed cosine similarity search.
5. **API Creation**: Built `/recommend` endpoint with FastAPI that returns 1–10 relevant assessments based on a score threshold.
6. **Frontend**: Built both Streamlit and pure HTML/JS frontend for interaction with the API.
7. **Deployment**: Backend on Render, frontend on GitHub Pages.

---

## Code Overview

| File | Purpose |
|------|---------|
| [`catalog_scraping.py`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/catalog_scraping.py) | Scrapes SHL product catalog across multiple pages |
| [`preprocess_embeddings.py`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/preprocess_embeddings.py) | Constructs embedding text and generates OpenAI embeddings |
| [`main.py`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/main.py) | FastAPI backend with FAISS search and `/recommend` endpoint |
| [`models.py`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/models.py) | Pydantic models for API request/response |
| [`app.py`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/app.py) | Optional Streamlit-based UI for testing the recommendation system |
| [`index.html`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/index.html) | Simple HTML/JS frontend for API interaction |
| [`generate_predictions.py`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/generate_predictions.py) | Generates predictions for test set |
| [`requirements.txt`](https://github.com/metechmohit/Assessment-Recommender-System/blob/main/requirements.txt) | Python dependencies |

---

## Live Demo Links

- **Frontend (HTML/CSS)**: [Try Frontend](https://metechmohit.github.io/shl-recommendation-frontened/)
- **FastAPI Docs (Swagger UI)**: [View Swagger](https://shl-recommender-system.onrender.com/docs)
- **Sample API Endpoint**:  
  - Health Check Endpoint (GET): [https://shl-recommender-system.onrender.com/health](https://shl-recommender-system.onrender.com/health)
  - Assessment Recommendation Endpoint (POST): https://shl-recommender-system.onrender.com/recommend

> You can customize the `query` parameter for different use cases.

---

## Features

- Accepts natural language queries, job description text, or a URL containing a JD
- Semantic vector search using OpenAI’s `text-embedding-3-small`
- FAISS-powered fast top-k assessment retrieval
- Relevance filtering based on score threshold (min 1, max 10 results)
- REST API architecture (JSON output)
- CORS-enabled and publicly accessible (for assessment testing)
- Deployed backend (Render) + two frontend options (Streamlit & Static)

---

## Tech Stack

| Layer         | Tools/Libraries                     |
|---------------|-------------------------------------|
| Scraping      | `Selenium`, `BeautifulSoup`         |
| Processing    | `pandas`, `numpy`                   |
| Embeddings    | `OpenAI API` (`text-embedding-3-small`) |
| Vector Search | `FAISS` (`faiss-cpu`)               |
| API Backend   | `FastAPI`, `Uvicorn`                |
| Frontend      | `HTML/CSS/JS`, `Streamlit`          |
| Deployment    | `Render`, `GitHub Pages`            |

---

## Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/metechmohit/Assessment-Recommender-System
cd Assessment-Recommender-System
pip install -r requirements.txt
```
### 2. Create a .env file with:
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx
```
### 3. Run FastAPI server
```bash
uvicorn main:app --reload
```
### 4. Run Streamlit app
```bash
streamlit run app.py
```
### 5. Run HTML/JS frontend
Open `index.html` in your browser or visit the deployed [frontend link](https://metechmohit.github.io/shl-recommendation-frontened/).

---

## API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /recommend`
Get assessment recommendations.

**Request:**
```json
{
  "query": "Looking for Python and SQL developers"
}
```

**Response:**
```json
{
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/...",
      "adaptive_support": "Yes",
      "description": "Multi-choice test...",
      "duration": 11,
      "remote_support": "Yes",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
```
- Add `frontend=true` as a query parameter for a frontend-friendly format.

---

## Sample Queries (from official PDF)

- I am hiring for Java developers who can also collaborate effectively with my business teams.
- Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script.
- Here is a JD text, can you recommend some assessment that can help me screen applications. I am hiring for an analyst and wants applications to screen using Cognitive and personality tests

---



