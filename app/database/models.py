from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database.base import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    qr_url = Column(String, nullable=True)
    campaign_id = Column(Integer, nullable=True)

    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    status = Column(String, default="offline")  # online/offline
    created_at = Column(DateTime, default=datetime.utcnow)
