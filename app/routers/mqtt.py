from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.mqtt_service import MQTTService

router = APIRouter()
mqtt_service = MQTTService()

class MessageRequest(BaseModel):
    topic: str
    message: str

@router.post("/publish")
def publish_message(request: MessageRequest):
    try:
        mqtt_service.publish(request.topic, request.message)
        return {"status": "success", "topic": request.topic, "message": request.message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
