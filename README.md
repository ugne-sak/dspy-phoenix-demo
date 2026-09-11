# DSPy pipeline → Phoenix

## 1. Start Phoenix

```bash
PHOENIX_WORKING_DIR=./.phoenix uv run phoenix serve
```

## 2. Run the pipeline

```bash
uv run run.py
```

## 3. Run the app

```bash
uv run uvicorn app:app --reload --port 8001
```

```bash
curl -G http://localhost:8001/ask --data-urlencode "question=Why is the sky blue?"
```
