from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import numpy as np

# ---------------------------
# App init
# ---------------------------
app = FastAPI(title="News Classification API (TF-IDF + LR)")

# ---------------------------
# Load model & vectorizer ONCE
# ---------------------------
model = joblib.load(
    "D:\\scrapy\\newsscrapper\\newsscrapper\\logistic_regression_model.pkl"
)
vectorizer = joblib.load(
    "D:\\scrapy\\newsscrapper\\newsscrapper\\tfidf_vectorizer.pkl"
)

# ---------------------------
# Label mapping
# ---------------------------
id2label = {
    0: "lifestyle",
    1: "education",
    2: "sports",
    3: "entertainment",
    4: "business"
}

# ---------------------------
# Request / Response schema
# ---------------------------
class NewsInput(BaseModel):
    title: str
    content: str

class PredictionResponse(BaseModel):
    category: str
    confidence: float

# ---------------------------
# Prediction endpoint
# ---------------------------
@app.post("/predict", response_model=PredictionResponse)
def predict(news: NewsInput):

    # Combine title + content (same as training)
    text = news.title + " " + news.content

    # TF-IDF transform
    X = vectorizer.transform([text])

    # Predict probabilities
    probs = model.predict_proba(X)[0]
    pred_id = np.argmax(probs)

    return {
        "category": id2label[pred_id],
        "confidence": round(float(probs[pred_id]), 4)
    }

# ---------------------------
# Serve Frontend UI
# ---------------------------
app.mount(
    "/", 
    StaticFiles(directory="frontend", html=True), 
    name="frontend"
)
