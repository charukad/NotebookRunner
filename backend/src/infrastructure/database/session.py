import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Expects DB URL from environment or uses default for local docker
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/notebookrunner")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
