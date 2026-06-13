# ML Sentiment App

A production-ready sentiment analysis microservice built with **FastAPI** and **TextBlob**. This project demonstrates modern DevOps practices including CI/CD pipelines, containerization, code quality automation, and observability with Prometheus metrics.

> **Course:** CISC-814 — DevOps & CI/CD  
> **Team:** Marwan Aly, Manar Elabsi, Mohamed Othman, Aya Abdallah

---

## Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   HTTP Client   │──────▶   FastAPI App   │──────▶   TextBlob ML   │
│   (curl, UI)    │      │   (inference)   │      │   (predict)     │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Prometheus     │
                       │  Metrics        │
                       │  (/metrics)     │
                       └─────────────────┘
```

**Pipeline:**
```
Code Push ──▶ Lint (ruff) ──▶ Type Check (mypy) ──▶ Test (pytest) ──▶ Build (Docker) ──▶ Push (Registry)
```

---

## Features

- **Sentiment Analysis** — Classifies text as `positive`, `negative`, or `neutral` with confidence scores
- **REST API** — Clean FastAPI endpoints with Pydantic validation and automatic OpenAPI docs
- **Observability** — Prometheus metrics for request counts, latency histograms, and label distribution
- **Input Validation** — URL/HTML stripping, whitespace normalization, empty string rejection
- **Health Checks** — `/health` endpoint for container orchestration readiness
- **100% Test Coverage** — Unit and integration tests with pytest and pytest-cov
- **Multi-Stage Docker** — Slim, secure image with non-root user
- **CI/CD Ready** — Gitea workflow with lint, type-check, test, build, and SBOM generation

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web Framework | FastAPI 0.115.6 | High-performance async API |
| ML/NLP | TextBlob 0.18.0 | Sentiment polarity analysis |
| Validation | Pydantic 2.10.4 | Request/response schema validation |
| Metrics | prometheus-client 0.21.1 | Observability & monitoring |
| Server | Uvicorn 0.34.0 | ASGI server |
| Linting | Ruff 0.8.6 | Fast Python linting & formatting |
| Type Checking | mypy 1.14.1 | Static type analysis |
| Testing | pytest 8.3.4 + pytest-cov 6.0.0 | Unit & integration tests |
| Container | Docker + multi-stage build | Secure, minimal image |

---

## Project Structure

```
ml-sentiment-app/
├── src/
│   ├── __init__.py          # Package marker
│   ├── inference.py         # FastAPI app, routes, Prometheus metrics
│   ├── model.py             # TextBlob sentiment prediction logic
│   └── preprocess.py        # Text cleaning & input validation
├── tests/
│   ├── __init__.py
│   ├── test_inference.py    # FastAPI endpoint integration tests
│   ├── test_model.py         # Sentiment model unit tests
│   └── test_preprocess.py    # Preprocessing utility tests
├── .gitea/workflows/
│   └── ci.yml               # CI pipeline (lint, type-check, test, build, sbom)
├── Dockerfile               # Multi-stage build with non-root user
├── .dockerignore            # Build context exclusions
├── pyproject.toml           # Tool configs (ruff, mypy, pytest)
├── requirements.txt         # Python dependencies
├── .gitignore               # Git exclusions
├── TASKS.md                 # Team task distribution
└── README.md                # This file
```

---

## API Documentation

### Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/health` | Health check | — |
| `GET` | `/metrics` | Prometheus metrics | — |
| `POST` | `/predict` | Sentiment prediction | `{ "text": "..." }` |

### `POST /predict`

**Request:**
```json
{
  "text": "I absolutely love this product!"
}
```

**Response (200):**
```json
{
  "label": "positive",
  "confidence": 0.7
}
```

**Response (400 — Invalid Input):**
```json
{
  "detail": "Invalid input text"
}
```

**Response (422 — Missing Field):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "text"],
      "msg": "Field required"
    }
  ]
}
```

**Response (500 — Server Error):**
```json
{
  "detail": "Simulated 500 error for testing"
}
```
> Trigger with `{"text": "__TEST_500__"}` for error-rate testing.

---

## Local Setup

### Prerequisites
- Python 3.11+
- pip or virtualenv

### 1. Clone & Create Virtual Environment

```bash
cd ml-sentiment-app
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 3. Run the Server

```bash
uvicorn src.inference:app --reload
```

Server starts at: **`http://127.0.0.1:8000`**

Interactive docs: **`http://127.0.0.1:8000/docs`**

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Predict sentiment
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'

# View metrics
curl http://localhost:8000/metrics
```

---

## Docker

### Build

```bash
docker build -t ml-sentiment-app:latest .
```

### Run

```bash
docker run -p 8000:8000 ml-sentiment-app:latest
```

### Verify

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text": "Great service!"}'
```

### Docker Image Details

- **Base:** `python:3.11-slim`
- **User:** Non-root (`appuser`)
- **Stages:** 2-stage build (builder → runtime)
- **Port:** `8000`
- **Size:** ~150 MB (optimized)

---

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Test Files

| File | What It Tests |
|------|---------------|
| `test_inference.py` | FastAPI routes, health, predict, error handling, edge cases |
| `test_model.py` | Positive, negative, neutral sentiment, structure, long text |
| `test_preprocess.py` | URL removal, HTML stripping, whitespace, input validation |

### Code Quality

```bash
# Linting
ruff check src/ tests/

# Type checking
mypy src/

# Format (auto-fix)
ruff check src/ tests/ --fix
```

---

## CI/CD Pipeline

The `.gitea/workflows/ci.yml` runs on every push and PR to `main`:

```
┌─────────┐   ┌──────────┐   ┌───────┐   ┌─────────────┐   ┌──────┐
│  lint   │──▶│type-check│──▶│  test │──▶│build & push │──▶│ sbom │
│  (ruff) │   │ (mypy)   │   │(pytest)│   │  (Docker)   │   │(SPDX)│
└─────────┘   └──────────┘   └───────┘   └─────────────┘   └──────┘
```

### Jobs

1. **lint** — Ruff checks code style and imports
2. **type-check** — mypy validates type annotations
3. **test** — pytest with coverage reporting (target: 100%)
4. **build-and-push** — Multi-stage Docker build, push to `cisc814-registry:5000/ml-sentiment-app`
5. **sbom** — Generates SPDX SBOM artifact for supply chain security

### Registry

- **URL:** `cisc814-registry:5000`
- **Image:** `ml-sentiment-app:latest`
- **Tag:** Git commit SHA

---

## Team & Responsibilities

| Member | Role | Contributions |
|--------|------|-------------|
| **Marwan Aly** | CI Pipeline | `.gitea/workflows/ci.yml`, registry config, pipeline orchestration |
| **Manar Elabsi** | Code Quality | Fixed mypy annotations in `preprocess.py` & `inference.py`, ruff compliance |
| **Mohamed Othman** | Testing | Edge-case tests, integration tests, maintained 100% coverage |
| **Aya Abdallah** | DevOps | Multi-stage Dockerfile, `.dockerignore`, non-root user, SBOM |

---

## Configuration

### `pyproject.toml`

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true

[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing"
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHONPATH` | `/app` | Python module path (Docker) |
| `NLTK_DATA` | `/home/appuser/nltk_data` | TextBlob corpora location |
| `PATH` | `...` | Includes user-local pip bin |

---

## License

Academic project for CISC-814. Not for production use without review.

---

## Quick Reference

```bash
# Start dev server
uvicorn src.inference:app --reload

# Run tests
pytest

# Check quality
ruff check src/ tests/ && mypy src/

# Build & run Docker
docker build -t ml-sentiment-app . && docker run -p 8000:8000 ml-sentiment-app

# Test prediction
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text": "Hello!"}'
```
