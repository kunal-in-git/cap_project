"""FastAPI app exposing an LLM-powered /ask endpoint (LangChain + Ollama)."""

from fastapi import FastAPI
from pydantic import BaseModel

from chain import ask, model_name

app = FastAPI(title="LLM Q&A Service")


class AskRequest(BaseModel):
    question: str
    context: str = ""
    session_id: str = "default"


class AskResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest) -> AskResponse:
    answer = ask(request.question, request.context, request.session_id)
    return AskResponse(answer=answer)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": model_name()}
