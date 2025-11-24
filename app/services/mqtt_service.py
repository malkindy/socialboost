# app/services/mqtt_service.py

import json
import asyncio
import paho.mqtt.client as mqtt

from app.config import Settings
from app.database.session import SessionLocal
from app.database.models import Device
#from app.routers.ws_devices import broadcast  # WebSocket broadcast function


settings = Settings()


class MQTTService:
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()

        # MQTT event handlers
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = lambda client, userdata, level, buf: print("[MQTT LOG]", buf)

        self.connect()

    # -----------------------------------------------------------
    # CONNECT TO BROKER
    # -----------------------------------------------------------
    def connect(self):
        """Connect to the MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)

            # Start MQTT background thread
            self.client.loop_start()

            print(f"[MQTT] Connected to broker at {self.broker_host}:{self.broker_port}")
        except Exception as e:
            print(f"[MQTT] Connection failed: {e}")

    # -----------------------------------------------------------
    # ON CONNECT — SUBSCRIPTIONS
    # -----------------------------------------------------------
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] Connection OK")

            # Subscribe to ALL device status topics
            self.client.subscribe("socialboost/device/+/status")
            print("[MQTT] Subscribed to device status updates")

        else:
            print(f"[MQTT] Connection failed with code {rc}")

    # -----------------------------------------------------------
    # ON MESSAGE — HANDLE DEVICE STATUS UPDATES
    # -----------------------------------------------------------
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        print(f"[MQTT] Received on {topic}: {payload}")

        # Topic example: socialboost/device/3/status
        if "device" in topic and "status" in topic:
            try:
                parts = topic.split("/")
                device_id = int(parts[2])
                data = json.loads(payload)

                status = data.get("status")
                if status not in ["online", "offline"]:
                    print("[MQTT] Invalid status payload")
                    return

                # Update DB
                db = SessionLocal()
                device = db.query(Device).filter(Device.id == device_id).first()
                if device:
                    device.status = status
                    db.commit()
                db.close()

                # Broadcast to frontend WebSockets
                asyncio.create_task(
                    broadcast({
                        "device_id": device_id,
                        "status": status
                    })
                )

                print(f"[MQTT] Device {device_id} status updated → {status}")

            except Exception as e:
                print("[MQTT] Error processing device status:", e)

    # -----------------------------------------------------------
    # PUBLISH MESSAGES
    # -----------------------------------------------------------
    def publish(self, topic: str, message: str):
        """Publish a message to a topic"""
        result = self.client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"[MQTT] Sent `{message}` to topic `{topic}`")
        else:
            print(f"[MQTT] Failed to send message to topic {topic}")
