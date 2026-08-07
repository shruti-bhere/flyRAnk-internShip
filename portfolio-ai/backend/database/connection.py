from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.core.config import settings

# Initialize the SQLAlchemy Engine using our dynamically generated URL config
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping checks the connection health before executing statements
    pool_pre_ping=True
)

# Establish an isolated, thread-safe session factory configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class that maps our Python classes directly to database tables
Base = declarative_base()

def get_db():
    """
    Dependency provider that yields a transaction database session context 
    and guarantees structural closing when operations terminate.
```python
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        """