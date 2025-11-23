from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.database.models import Device
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for API response
class DeviceOut(BaseModel):
    id: int
    name: str
    status: str

    class Config:
        orm_mode = True

# GET all devices
@router.get("/", response_model=List[DeviceOut])
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices
