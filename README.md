# Autonomous AI Document Generation Agent

An autonomous AI agent built with FastAPI and LangChain that:

- Understands natural language requests
- Creates its own execution plan
- Executes each step autonomously
- Generates professional Microsoft Word (.docx) documents

## Tech Stack

- Python
- FastAPI
- LangChain
- Groq
- python-docx

## Run

```bash
uv sync
uv run uvicorn main:app --reload
```

API

POST

```
/agent
```

Example

```json
{
    "request":"Create a project proposal for an AI-powered HR Management System."
}
```