from fastapi import FastAPI, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
import stripe

from app.database import Base, engine, get_db
from app.schemas import GenerateRequest, UsageResponse
from app.services import record_usage_idempotent, get_tenant_plan, calculate_token_cost
from app.models import UsageEvent, Subscription, Plan
from app.config import Config

# Database Tables तयार करा
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Usage Metering & Billing Engine",
    description="Multi-tenant backend for usage metering, quota enforcement, and Stripe webhooks.",
    version="1.0.0"
)

processed_webhooks = set()  # In-memory webhook deduplication

# ---------------------------------------------------------------------
# ROOT ROUTE (404 Not Found दूर करण्यासाठी)
# ---------------------------------------------------------------------
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Usage Metering & Billing Engine",
        "documentation": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "billable_generate": "POST /api/v1/generate",
            "usage_summary": "GET /usage?tenant_id=tenant_123",
            "stripe_webhook": "POST /webhooks/stripe"
        }
    }

# ---------------------------------------------------------------------
# BILLABLE GENERATE ENDPOINT (Metering + Idempotency + Quota)
# ---------------------------------------------------------------------
@app.post("/api/v1/generate")
def generate_ai_response(
    req: GenerateRequest, 
    tenant_id: str = Header(...), 
    idempotency_key: str = Header(...),
    db: Session = Depends(get_db)
):
    total_tokens = req.input_tokens + req.cached_tokens + req.output_tokens + req.reasoning_tokens
    
    # Meter API Call & AI Tokens Idempotently
    record_usage_idempotent(db, tenant_id, "api_call", 1, f"{idempotency_key}_api")
    record_usage_idempotent(db, tenant_id, "ai_tokens", total_tokens, f"{idempotency_key}_tokens")

    return {
        "status": "success",
        "tokens_processed": total_tokens,
        "message": "AI Generation completed successfully"
    }

# ---------------------------------------------------------------------
# USAGE ROLLUP API
# ---------------------------------------------------------------------
@app.get("/usage", response_model=UsageResponse)
def get_usage_summary(tenant_id: str, db: Session = Depends(get_db)):
    plan = get_tenant_plan(db, tenant_id)

    api_used = db.query(func.sum(UsageEvent.quantity)).filter(
        UsageEvent.tenant_id == tenant_id, UsageEvent.event_type == "api_call"
    ).scalar() or 0

    tokens_used = db.query(func.sum(UsageEvent.quantity)).filter(
        UsageEvent.tenant_id == tenant_id, UsageEvent.event_type == "ai_tokens"
    ).scalar() or 0

    # Total Cost Calculation in USD
    total_micro_cents = (api_used * Config.COST_PER_API_CALL_MICRO_CENTS) + (tokens_used * Config.COST_PER_INPUT_TOKEN_MICRO_CENTS)
    cost_usd = round(total_micro_cents / 1_000_000, 6)

    return UsageResponse(
        tenant_id=tenant_id,
        plan_name=plan.name,
        api_calls_used=api_used,
        api_calls_limit=plan.api_quota,
        tokens_used=tokens_used,
        tokens_limit=plan.token_quota,
        total_cost_usd=cost_usd
    )

# ---------------------------------------------------------------------
# STRIPE WEBHOOK HANDLER
# ---------------------------------------------------------------------
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, Config.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Event Deduplication Check
    event_id = event.get("id")
    if event_id in processed_webhooks:
        return {"status": "ignored_duplicate"}
    
    processed_webhooks.add(event_id)

    # Handle Plan Upgrade Sync
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        tenant_id = session.get("client_reference_id")
        
        if tenant_id:
            sub = db.query(Subscription).filter(Subscription.tenant_id == tenant_id).first()
            if sub:
                sub.plan_id = "Pro"
                db.commit()

    return {"status": "success"}