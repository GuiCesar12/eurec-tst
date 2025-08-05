from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
import os
from typing import Optional

def get_database_url() -> str:
    host = os.getenv('DATABASE_HOST', 'db')
    user = os.getenv('POSTGRES_USER', 'user')
    password = os.getenv('POSTGRES_PASSWORD', 'password')
    db_name = os.getenv('POSTGRES_DB', 'publications')
    
    return f"postgresql://{user}:{password}@{host}:5432/{db_name}"
def create_db_engine():
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,  # Verifica conexões antes de usar
        pool_size=10,
        max_overflow=20
    )

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cria tabelas apenas se não estiver sendo importado por outro módulo
if __name__ != "__main__":
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create tables - {str(e)}")