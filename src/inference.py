"""Edit FastAPI inference server for sentiment analysis."""

import time

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import BaseModel

from src.model import predict_sentiment
from src.preprocess import validate_input

app = FastAPI(title="ML Sentiment Analyzer", version="0.1.0")

prediction_requests_total = Counter(
    "prediction_requests_total",
    "Total number of prediction requests",
    ["method", "endpoint", "status"],
)

predictions_by_label_total = Counter(
    "predictions_by_label_total",
    "Total predictions per sentiment label",
    ["label"],
)

prediction_latency_seconds = Histogram(
    "prediction_latency_seconds",
    "Prediction request latency in seconds",
    ["method", "endpoint"],
)


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str
    confidence: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/metrics")
def metrics() -> Response:
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type="text/plain")


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    start = time.time()
    if not validate_input(request.text):
        prediction_requests_total.labels(
            method="POST", endpoint="/predict", status="400"
        ).inc()
        raise HTTPException(status_code=400, detail="Invalid input text")
    try:
        # Test trigger for error rate panel
        # Send JSON: {"text": "__TEST_500__"} to simulate a 500 error
        if request.text == "__TEST_500__":
            raise RuntimeError("Simulated 500 error for testing")

        result = predict_sentiment(request.text)
        duration = time.time() - start
        prediction_latency_seconds.labels(
            method="POST", endpoint="/predict"
        ).observe(duration)
        prediction_requests_total.labels(
            method="POST", endpoint="/predict", status="200"
        ).inc()
        predictions_by_label_total.labels(label=result["label"]).inc()
        return PredictResponse(label=result["label"], confidence=result["confidence"])
    except Exception as e:
        prediction_requests_total.labels(
            method="POST", endpoint="/predict", status="500"
        ).inc()
        raise HTTPException(status_code=500, detail=str(e)) from e
