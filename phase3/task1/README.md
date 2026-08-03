# Task A — FastAPI + LangChain LLM Service (Dockerized)

A FastAPI app with an LLM-powered `/ask` endpoint: a LangChain chain (system prompt → question + context → LLM) backed by a local **Ollama** model (`llama3.1:8b`), with per-session conversation memory. Containerized with Docker, running on port 8001.

## Why a local model
No Anthropic/OpenAI API key was available in the build environment. Ollama was already installed locally with `llama3.1:8b` pulled, so the chain targets that instead of a paid API — the LLM backend is swappable via the `LLM_MODEL`/`OLLAMA_BASE_URL` env vars in `chain.py` if you'd rather point it at a hosted model.

## Files
- `main.py` — FastAPI app: `POST /ask`, `GET /health`
- `chain.py` — the LangChain chain and per-session memory (`RunnableWithMessageHistory`)
- `Dockerfile` — `python:3.11-slim`, installs `requirements.txt`, runs on port 8001
- `requirements.txt`

## API

**`POST /ask`**
```json
{ "question": "string", "context": "string", "session_id": "string (optional, default \"default\")" }
```
→ `{ "answer": "string" }`

`session_id` is an addition beyond the spec's exact body shape — it's optional and defaults to `"default"`, so the required `{question, context}` shape still works as-is; it's what lets multiple independent conversations be remembered at once instead of one global history.

**`GET /health`** → `{ "status": "ok", "model": "llama3.1:8b" }`

## Conversation memory
Each `session_id` gets its own in-memory chat history (`InMemoryChatMessageHistory`), so a later `/ask` call with the same `session_id` sees prior Q&A turns even though HTTP itself is stateless. Memory does not persist across container restarts (in-process dict) — that's fine for this demo but would need a real store (Redis, a DB) for production use.

## Running it

### With Docker
```bash
docker build -t phase3-llm-service .
docker run -d -p 8001:8001 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 phase3-llm-service
```
`host.docker.internal` is Docker Desktop's DNS name for reaching a service (Ollama) running on the host machine, not inside the container. Requires `ollama serve` running on the host with the model pulled (`ollama pull llama3.1:8b`).

### Without Docker
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Verified end-to-end (actually run, both bare-metal and in Docker)
```
$ curl http://127.0.0.1:8001/health
{"status":"ok","model":"llama3.1:8b"}

$ curl -X POST http://127.0.0.1:8001/ask -d '{"question":"What is the capital of France?","context":"Paris is the capital of France.","session_id":"demo"}'
{"answer":"The capital of France is Paris."}

$ curl -X POST http://127.0.0.1:8001/ask -d '{"question":"What did I just ask you?","context":"","session_id":"demo"}'
{"answer":"You asked me what the capital of France is."}
```
The second call has no context and a different question, yet correctly recalls the first turn — confirming the per-session memory works, not just the raw chain.

## Testing via Swagger UI (`/docs`)
`GET /docs` and `GET /openapi.json` both returned `200` from the running container, confirming Swagger UI serves correctly. **No screenshot is included**: this was built in a headless sandbox with no display (`screencapture` fails with "could not create image from display", the same constraint that blocked downloading a headless-browser binary elsewhere in this project) — there was no way to actually render and capture a browser window here. Swagger UI's "Try it out" sends the exact same HTTP request as the `curl` calls above, so the verified output is equivalent; it just isn't a screenshot.

To capture the actual screenshot yourself: run the container, open `http://localhost:8001/docs`, expand `POST /ask`, click **Try it out**, paste the JSON body above, click **Execute**, and screenshot the response panel.

## Bonus
`GET /health` returns `{"status": "ok", "model": "llama3.1:8b"}` as required.
