# Customer Support Chatbot (FastAPI + Ollama)

A minimal FastAPI service that proxies customer support queries to an Ollama model (default: deepseek-r1) and returns a simple text response. Includes typed request/response models, async HTTP, CORS, and a health endpoint.

## Quickstart

1) Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Configure environment (optional)

```bash
cp .env.example .env
# adjust values as needed
```

Environment variables used by the API:
- OLLAMA_URL (default: http://localhost:11434/api/generate)
- MODEL_NAME (default: deepseek-r1)
- REQUEST_TIMEOUT_SECS (default: 30)

4) Run the API

```bash
uvicorn app:app --reload --port 8000
```

## Endpoints

- GET /health
- POST /chatbot

Example request:

```bash
curl -sS -X POST 'http://localhost:8000/chatbot' \
  -H 'Content-Type: application/json' \
  -d '{"query": "How do I return an item?", "language": "English"}'
```

Example response:

```json
{"response": "You can initiate a return within 30 days ..."}
```

## Notes
- Ensure Ollama is running locally and the specified model is pulled.
- The legacy Gradio script in `customer_support_bot.py` is unchanged. We can refactor it next to call this API or modernize it with `gradio>=4` and env config.
