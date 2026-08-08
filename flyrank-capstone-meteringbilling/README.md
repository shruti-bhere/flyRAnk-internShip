# ⚡ Usage Metering & Billing Engine

A multi-tenant backend service designed to solve usage metering, quota enforcement, precise money arithmetic (token cost calculation), and signature-verified Stripe webhook integrations. Built to ensure **exactly-once execution** (idempotency) and zero double-counting under retries or network failures.

---

## 📌 Project Overview

Billing systems demand absolute correctness. A single retry error or double-counted request can double-charge customers or grant unlimited unauthorized access. This Capstone implements a robust metering engine handling four core backend concerns:

1. **Idempotent Metering:** Deduplicates incoming billable requests using a unique `Idempotency-Key` header.
2. **Quota Enforcement:** Evaluates usage boundaries before execution and yields explicit `429 Too Many Requests` or `402 Payment Required` HTTP responses upon limit breach.
3. **Integer Money Math:** Eliminates floating-point inaccuracies by storing costs in micro-cents. Implements real-world LLM token pricing (cached, output, and reasoning tokens).
4. **Stripe Test Mode Integration:** Handles subscription lifecycle updates via signature-verified, deduplicated Stripe webhooks.

---

## 🛠️ Tech Stack & Requirements

* **Language & Framework:** Python 3.10+ / FastAPI
* **Database:** PostgreSQL (Docker containerized)
* **ORM:** SQLAlchemy (with Unique Constraints for Idempotency)
* **Payment Integration:** Stripe API & Stripe CLI (Test Mode)
* **Testing:** Pytest (Unit & Integration tests)

---
-> How start this Assignment 

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

docker compose up -d

python scripts/seed.py

uvicorn app.main:app --reload

Running Acceptance Tests
python -m pytest tests/test_billing_engine.py -v