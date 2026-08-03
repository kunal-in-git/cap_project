"""LangChain chain: system prompt -> user question with context -> LLM,
with per-session conversation memory.
"""

import os

from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

MODEL_NAME = os.environ.get("LLM_MODEL", "llama3.1:8b")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

SYSTEM_PROMPT = (
    "You are a helpful assistant. Use the provided context to answer the "
    "user's question accurately and concisely. If the context doesn't "
    "contain the answer, say so instead of guessing."
)

_llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=0)

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "Context: {context}\n\nQuestion: {question}"),
    ]
)

_chain = _prompt | _llm

_session_histories: dict[str, BaseChatMessageHistory] = {}


def _get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _session_histories:
        _session_histories[session_id] = InMemoryChatMessageHistory()
    return _session_histories[session_id]


chain_with_memory = RunnableWithMessageHistory(
    _chain,
    _get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


def ask(question: str, context: str, session_id: str) -> str:
    """Run the chain for one question, remembering prior turns in `session_id`."""
    response = chain_with_memory.invoke(
        {"question": question, "context": context},
        config={"configurable": {"session_id": session_id}},
    )
    return response.content


def model_name() -> str:
    return MODEL_NAME
