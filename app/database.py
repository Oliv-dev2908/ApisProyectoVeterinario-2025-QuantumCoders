from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

if not SUPABASE_DB_URL:
    raise ValueError("SUPABASE_DB_URL no fue seteada")

engine = create_engine(SUPABASE_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()