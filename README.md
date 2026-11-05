# AI Ops Suite

Customer-operations platform where the LLM proposes and deterministic code decides.

## Setup
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env

## Run
uvicorn app.main:app --reload

## Test
pytest