import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5433/billing_db")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_dummy")

    # Pricing Constants (in Micro-Cents to avoid floating point bugs)
    # 1 Cent = 10,000 Micro-cents
    COST_PER_API_CALL_MICRO_CENTS = 100               # $0.00001
    COST_PER_INPUT_TOKEN_MICRO_CENTS = 15             # $0.0000015
    COST_PER_CACHED_TOKEN_MICRO_CENTS = 5             # $0.0000005
    COST_PER_OUTPUT_TOKEN_MICRO_CENTS = 60            # $0.0000060
    COST_PER_REASONING_TOKEN_MICRO_CENTS = 60         # Billed same as output token