# AI Ops Suite

A product-oriented customer-operations platform. The core safety principle is:

> The model proposes; deterministic application code validates and executes.

The current foundation provides a FastAPI service, PostgreSQL persistence, an explicit SQL migration runner, a deterministic issue-triage baseline, and automated tests. It does not yet execute refunds or call external commerce systems.

## Requirements

- Python 3.11+
- Docker Desktop / Docker Engine with Compose (recommended for local PostgreSQL)

## Run locally with Docker

```bash
docker compose up --build
```

The API is available at http://localhost:8000. PostgreSQL is initialized from
`app/db/migrations/001_init.sql` when the database volume is first created.

Useful endpoints:

- `GET /health` — API process health
- `GET /health/db` — database connectivity
- `POST /api/v1/triage` — deterministic support-message classification

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{"message":"My product arrived damaged","order_id":"ORD-100"}'
```

## Run locally with an existing PostgreSQL database

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
python -m scripts.migrate
uvicorn app.main:app --reload
```

Set `DATABASE_URL` in `.env` to your PostgreSQL connection string. The migration runner records applied SQL files in `schema_migrations`.

## Test and lint

```bash
pytest -q
ruff check app tests scripts
```

## Current scope and next milestones

1. **Foundation (current):** API, database schema/lifecycle, migrations, typed triage contract, deterministic triage, CI.
2. **Workflow core:** persisted conversations/messages, deterministic state machine, customer/order lookup, audit events.
3. **Policy-backed actions:** refund eligibility rules, approval gates, idempotent simulated refund tool.
4. **Knowledge and agents:** policy RAG, grounded answers, specialized agent interfaces.
5. **Product experience:** operations dashboard, human review queue, metrics and observability.
6. **Hardening:** authorization, tenant isolation, evaluation suite, deployment and operational runbooks.

External actions must remain behind application-side policy checks and explicit authorization. The triage endpoint currently classifies messages only; it does not access customer records or initiate transactions.
