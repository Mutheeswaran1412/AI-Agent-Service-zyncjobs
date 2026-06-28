# ZyncJobs AI Service

AI Agent Platform for ZyncJobs — Resume Builder, Parser, ATS Scoring, Job Matching, Career Coach, JD Generator, Interview Questions, and more.

## Architecture

```
User → FastAPI → Orchestrator → Agent → Tools → LLM Router → Ollama → Response
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## API Docs

http://localhost:8000/docs
