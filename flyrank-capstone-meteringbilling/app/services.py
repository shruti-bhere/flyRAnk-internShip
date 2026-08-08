import uuid
import stripe
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models import Tenant, Subscription, Plan, UsageEvent
from app.config import Config

stripe.api_key = Config.STRIPE_SECRET_KEY

def get_tenant_plan(db: Session, tenant_id: str) -> Plan:
    sub = db.query(Subscription).filter(Subscription.tenant_id == tenant_id, Subscription.status == "active").first()
    if not sub:
        raise HTTPException(status_code=404, detail="Active subscription not found")
    return sub.plan

def calculate_token_cost(input_t: int, cached_t: int, output_t: int, reasoning_t: int) -> int:
    """Calculates cost in Micro-Cents (Integer Math)"""
    cost = (
        (input_t * Config.COST_PER_INPUT_TOKEN_MICRO_CENTS) +
        (cached_t * Config.COST_PER_CACHED_TOKEN_MICRO_CENTS) +
        (output_t * Config.COST_PER_OUTPUT_TOKEN_MICRO_CENTS) +
        (reasoning_t * Config.COST_PER_REASONING_TOKEN_MICRO_CENTS)
    )
    return cost

def record_usage_idempotent(
    db: Session, 
    tenant_id: str, 
    event_type: str, 
    quantity: int, 
    idempotency_key: str
) -> UsageEvent:
    # 1. Check Idempotency Key
    existing_event = db.query(UsageEvent).filter(UsageEvent.idempotency_key == idempotency_key).first()
    if existing_event:
        return existing_event  # Return original without adding duplicate event

    # 2. Quota Check before inserting
    plan = get_tenant_plan(db, tenant_id)
    
    current_usage = db.query(func.sum(UsageEvent.quantity)).filter(
        UsageEvent.tenant_id == tenant_id,
        UsageEvent.event_type == event_type
    ).scalar() or 0

    limit = plan.api_quota if event_type == "api_call" else plan.token_quota
    
    if current_usage + quantity > limit:
        if current_usage >= limit:
            raise HTTPException(status_code=429, detail="Monthly usage quota exceeded. Please upgrade your plan.")
        raise HTTPException(status_code=402, detail="Payment or Plan Upgrade required to execute this request.")

    # 3. Create Event
    new_event = UsageEvent(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        event_type=event_type,
        quantity=quantity,
        idempotency_key=idempotency_key
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event