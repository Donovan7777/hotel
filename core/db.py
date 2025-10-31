# core/db.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modele.base import Base

# Enable SQLAlchemy logging (INFO level)
logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/Hotel"
    "?driver=ODBC Driver 17 for SQL Server"
    "&Trusted_Connection=yes"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,                 # ✅ print all SQL querie
    use_setinputsizes=False,
    future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db():
    """Create all tables (only if they don’t exist yet)."""
    Base.metadata.create_all(bind=engine)
