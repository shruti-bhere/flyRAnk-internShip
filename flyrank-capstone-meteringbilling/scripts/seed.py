import sys
import os

# Ensure root folder is added to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Plan, Tenant, Subscription

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Add Plans
free_plan = Plan(id="Free", name="Free Plan", api_quota=1000, token_quota=100000)
pro_plan = Plan(id="Pro", name="Pro Plan", api_quota=50000, token_quota=5000000)

db.merge(free_plan)
db.merge(pro_plan)

# Add Test Tenant
tenant = Tenant(id="tenant_123", name="Acme Corp")
subscription = Subscription(id="sub_123", tenant_id="tenant_123", plan_id="Free", status="active")

db.merge(tenant)
db.merge(subscription)

db.commit()
db.close()
print("✔ Database Seeded Successfully!")