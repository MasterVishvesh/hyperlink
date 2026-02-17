from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os


# -----------------------------
# DATABASE LOCATION
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "pdf_tracking.db")

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# -----------------------------
# ENGINE CONFIG (SQLite Safe)
# -----------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # prevents locking errors
    },
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# -----------------------------
# PDF LINK TABLE
# -----------------------------

class PDFLink(Base):
    __tablename__ = "pdf_links"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# -----------------------------
# PDF LOG TABLE (EVERY VISIT)
# -----------------------------

class PDFLog(Base):
    __tablename__ = "pdf_logs"

    id = Column(Integer, primary_key=True, index=True)

    token = Column(String, index=True, nullable=False)

    ip_address = Column(String)

    user_agent = Column(String)

    referer = Column(String)

    source = Column(String)

    visitor_id = Column(String)

    visit_time = Column(DateTime, default=datetime.utcnow)


# -----------------------------
# CREATE TABLES
# -----------------------------

Base.metadata.create_all(bind=engine)
