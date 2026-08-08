import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    stripe_customer_id = Column(String, nullable=True)
    
    subscriptions = relationship("Subscription", back_populates="tenant")
    usage_events = relationship("UsageEvent", back_populates="tenant")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(String, primary_key=True)  # 'Free', 'Pro'
    name = Column(String, nullable=False)
    api_quota = Column(Integer, nullable=False)
    token_quota = Column(Integer, nullable=False)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    plan_id = Column(String, ForeignKey("plans.id"), nullable=False)
    status = Column(String, default="active")
    
    tenant = relationship("Tenant", back_populates="subscriptions")
    plan = relationship("Plan")


class UsageEvent(Base):
    __tablename__ = "usage_events"

    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    event_type = Column(String, nullable=False) # 'api_call', 'ai_tokens'
    quantity = Column(Integer, nullable=False)
    idempotency_key = Column(String, nullable=False, unique=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    tenant = relationship("Tenant", back_populates="usage_events")

    __table_args__ = (
        UniqueConstraint('idempotency_key', name='uix_idempotency_key'),
    )