# Task A — FastAPI + LangChain LLM Service

A FastAPI application with an LLM-powered `/ask` endpoint, a LangChain chain with per-session conversation memory, and a Dockerfile — built and tested end-to-end.

## Files
- `main.py` — FastAPI app: `POST /ask`, `GET /health`
- `chain.py` — LangChain chain (system prompt → question+context → LLM) with per-session memory
- `Dockerfile` — Python 3.11 base image, installs `requirements.txt`, runs on port 8000
- `requirements.txt` — FastAPI, LangChain, `langchain-ollama`

## LLM backend
Uses a **local Ollama model** (`llama3.1:8b` by default) via `langchain-ollama`, so it runs with no API key. Override with the `LLM_MODEL` / `OLLAMA_BASE_URL` env vars.

## Running it locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama serve                 # in a separate terminal, if not already running
uvicorn main:app --reload --port 8000
```
Swagger UI at `http://localhost:8000/docs`.

## Running it in Docker
```bash
docker build -t llm-qa-service .
docker run -p 8000:8000 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 llm-qa-service
```
`host.docker.internal` is required so the container can reach Ollama running on the host machine (`localhost` inside the container refers to the container itself, not the host).

## Endpoints

### `POST /ask`
```json
{"question": "What is FastAPI?", "context": "FastAPI is a modern Python web framework.", "session_id": "s1"}
```
→ `{"answer": "..."}`

`session_id` is optional (defaults to `"default"`) and keys the in-memory conversation history — sequential calls with the same `session_id` remember prior Q&A in that session. Memory is a plain in-process dict, so it resets on restart and won't work across multiple worker processes.

### `GET /health`
```json
{"status": "ok", "model": "llama3.1:8b"}
```

## Verified working
Tested live, not just written:
- `/ask` returns real Ollama-generated answers using the provided context.
- Conversation memory confirmed: a follow-up question ("What did I just ask you about?") with the same `session_id` correctly recalled the prior turn.
- Both confirmed inside the built Docker container as well as running natively.

## AI-Generated Parts
Built with Claude (Anthropic) across 5 steps: the `/ask` endpoint scaffold, the LangChain chain, conversation memory (`RunnableWithMessageHistory`), the Dockerfile, and the `/health` bonus endpoint — each step verified by actually running the code before moving to the next.
