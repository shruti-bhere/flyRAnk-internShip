import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Plan, Tenant, Subscription, UsageEvent
from app.config import Config

# Test Database setup (In-Memory SQLite or Test Postgres)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Seed Plans
    free_plan = Plan(id="Free", name="Free Plan", api_quota=1000, token_quota=100000)
    pro_plan = Plan(id="Pro", name="Pro Plan", api_quota=50000, token_quota=5000000)
    db.add(free_plan)
    db.add(pro_plan)

    # Seed Test Tenant
    tenant = Tenant(id="tenant_test", name="Test Corp")
    sub = Subscription(id="sub_test", tenant_id="tenant_test", plan_id="Free", status="active")
    db.add(tenant)
    db.add(sub)

    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


# =====================================================================
# PROBE 1: Idempotency (Same key sent twice -> exactly one usage event)
# =====================================================================
def test_probe_1_idempotency_duplicate_prevention():
    headers = {
        "tenant-id": "tenant_test",
        "idempotency-key": "unique_key_001"
    }
    payload = {"input_tokens": 100, "cached_tokens": 0, "output_tokens": 50, "reasoning_tokens": 0}

    # First Call
    res1 = client.post("/api/v1/generate", json=payload, headers=headers)
    assert res1.status_code == 200

    # Retry Call with exact same Idempotency-Key
    res2 = client.post("/api/v1/generate", json=payload, headers=headers)
    assert res2.status_code == 200

    # Verify Usage DB has recorded only ONE set of events
    db = TestingSessionLocal()
    events_count = db.query(UsageEvent).filter(UsageEvent.tenant_id == "tenant_test").count()
    # 2 events per call (1 for api_call, 1 for ai_tokens) -> exactly 2 rows total, NOT 4
    assert events_count == 2
    db.close()


# =====================================================================
# PROBE 2: Quota Boundary (Honest 429 / 402 on limit exceeded)
# =====================================================================
def test_probe_2_quota_boundary_enforcement():
    db = TestingSessionLocal()
    # Manually fill quota up to 1000 (Free plan limit)
    event = UsageEvent(
        id="evt_max",
        tenant_id="tenant_test",
        event_type="api_call",
        quantity=1000,
        idempotency_key="fill_quota_key"
    )
    db.add(event)
    db.commit()
    db.close()

    # Request after limit reached
    headers = {
        "tenant-id": "tenant_test",
        "idempotency-key": "exceed_key_002"
    }
    payload = {"input_tokens": 10, "cached_tokens": 0, "output_tokens": 10, "reasoning_tokens": 0}

    res = client.post("/api/v1/generate", json=payload, headers=headers)
    assert res.status_code == 429
    assert "quota exceeded" in res.json()["detail"].lower()


# =====================================================================
# PROBE 3 & 4: Stripe Webhook (Signature Verification & Deduplication)
# =====================================================================
def test_probe_4_forged_webhook_rejection():
    # Send forged/invalid signature
    headers = {"stripe-signature": "t=123,v1=invalid_signature_hash"}
    res = client.post("/webhooks/stripe", content=b"{}", headers=headers)
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid signature"


# =====================================================================
# PROBE 5: Cost Calculation & Usage Rollup
# =====================================================================
def test_probe_5_cost_rollup_calculation():
    headers = {
        "tenant-id": "tenant_test",
        "idempotency-key": "cost_test_key"
    }
    payload = {"input_tokens": 1000, "cached_tokens": 500, "output_tokens": 200, "reasoning_tokens": 100}

    client.post("/api/v1/generate", json=payload, headers=headers)

    res = client.get("/usage?tenant_id=tenant_test")
    assert res.status_code == 200
    data = res.json()

    assert data["api_calls_used"] == 1
    assert data["tokens_used"] == 1800
    assert data["plan_name"] == "Free Plan"
    assert data["total_cost_usd"] > 0