from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class PDFLink(Base):
    __tablename__ = "pdf_links"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    file_name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PDFLog(Base):
    __tablename__ = "pdf_logs"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    ip_address = Column(String)
    user_agent = Column(Text)
    opened_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
