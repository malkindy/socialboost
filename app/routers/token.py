# app/routers/token.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import secrets

from app.database.session import SessionLocal
from app.database.models import Token
from app.utils.qr_generator import generate_qr_code
from app.services.mqtt_service import MQTTService

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize MQTT Service
mqtt_service = MQTTService()

# -----------------------------
# Existing endpoint: create a general token
# -----------------------------
@router.post("/create", summary="Create a token and QR code")
def create_token(campaign_id: int = 1, db: Session = Depends(get_db)):
    """
    Create a secure token, generate QR PNG + base64,
    save token in DB, and publish base64 QR via MQTT.
    """

    # 1️⃣ Generate a secure random token
    token_value = secrets.token_urlsafe(8)

    # 2️⃣ Construct URL encoded in QR
    qr_url = f"http://192.168.1.113:8000/tweet?token={token_value}"

    # 3️⃣ Generate QR code (save PNG + return base64)
    png_filename = f"{token_value}.png"
    qr_base64 = generate_qr_code(qr_url, save_path=png_filename)

    # 4️⃣ Store in DB
    db_token = Token(
        token=token_value,
        qr_url=qr_url,
        campaign_id=campaign_id,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    # 5️⃣ Send QR via MQTT
    topic = "socialboost/display"
    mqtt_service.publish(topic, qr_base64)

    return {
        "token": token_value,
        "qr_url": qr_url,
        "qr_base64": qr_base64,
        "png_file_saved_as": png_filename,
        "campaign_id": campaign_id,
        "mqtt_topic": topic,
    }

# -----------------------------
# New endpoint: send token to a specific device
# -----------------------------
@router.post("/send-token/{device_id}", summary="Send token to a device")
def send_token_to_device(
    device_id: int,
    campaign_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Generate a token + QR for a specific device,
    store it, and publish via MQTT to device-specific topic.
    """
    # 1️⃣ Generate token
    token_value = secrets.token_urlsafe(8)

    # 2️⃣ Construct URL
    qr_url = f"http://192.168.1.113:8000/tweet?token={token_value}"

    # 3️⃣ Generate QR code PNG + base64
    png_filename = f"{token_value}.png"
    qr_base64 = generate_qr_code(qr_url, save_path=png_filename)

    # 4️⃣ Store in DB
    db_token = Token(
        token=token_value,
        qr_url=qr_url,
        campaign_id=campaign_id,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    # 5️⃣ Publish QR via MQTT to device-specific topic
    topic = f"socialboost/display/{device_id}"
    mqtt_service.publish(topic, qr_base64)

    return {
        "device_id": device_id,
        "token": token_value,
        "qr_url": qr_url,
        "qr_base64": qr_base64,
        "png_file_saved_as": png_filename,
        "campaign_id": campaign_id,
        "mqtt_topic": topic,
    }
