# ML Sentiment App — Starter

A simple sentiment analysis microservice built with FastAPI and TextBlob.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m textblob.download_corpora
uvicorn src.inference:app --reload
```

## Endpoints

- `GET /health` — Health check
- `POST /predict` — Sentiment prediction (JSON body: `{"text": "..."}`)

## Running Tests

```bash
pytest
```

## Code Quality

```bash
ruff check src/ tests/
mypy src/
```

## CI Pipeline

The CI pipeline runs on every push and pull request to `main`.

### Jobs

1. **lint** — Runs `ruff` on `src/` and `tests/`
2. **type-check** — Runs `mypy` on `src/`
3. **test** — Runs `pytest` with coverage reporting
4. **build-and-push** — Builds Docker image and pushes to registry
5. **sbom** — Generates SPDX SBOM artifact

### Registry

Images are pushed to `cisc814-registry:5000/ml-sentiment-app`
