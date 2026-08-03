from fastapi import FastAPI
from pydantic import BaseModel

import chain

app = FastAPI(title="LLM Q&A Service")


class AskRequest(BaseModel):
    question: str
    context: str
    session_id: str = "default"


class AskResponse(BaseModel):
    answer: str


class HealthResponse(BaseModel):
    status: str
    model: str


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    answer = chain.ask(request.question, request.context, request.session_id)
    return AskResponse(answer=answer)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model=chain.model_name())
