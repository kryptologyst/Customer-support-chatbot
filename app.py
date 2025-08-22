from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
import httpx
from dotenv import load_dotenv

app = FastAPI(title="Customer Support Chatbot API", version="0.2.0")

# Configuration via environment variables
load_dotenv()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-r1")
REQUEST_TIMEOUT_SECS = float(os.getenv("REQUEST_TIMEOUT_SECS", "30"))

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="End-user question")
    language: Optional[str] = Field(
        default="English", description="Preferred response language"
    )


class ChatResponse(BaseModel):
    response: str

@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/chatbot", response_model=ChatResponse)
async def chatbot_response(body: ChatRequest) -> ChatResponse:
    prompt = f"Answer customer query in {body.language}:\n\n{body.query}"
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECS) as client:
            resp = await client.post(OLLAMA_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
            text = data.get("response") or "No answer available."
            return ChatResponse(response=text)
    except httpx.TimeoutException:
        return ChatResponse(response="Upstream model timed out. Please try again.")
    except httpx.HTTPStatusError as e:
        return ChatResponse(response=f"Upstream error: {e.response.status_code}")
    except Exception:
        return ChatResponse(response="Unexpected error while processing your request.")

# Run with: uvicorn app:app --reload
