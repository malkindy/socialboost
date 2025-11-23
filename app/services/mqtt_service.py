# app/mqtt_service.py

import paho.mqtt.client as mqtt
from app.config import Settings

settings = Settings()

class MQTTService:
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()

        # Optional: log activity
        self.client.on_log = lambda client, userdata, level, buf: print("[MQTT LOG]", buf)

        self.connect()

    def connect(self):
        """Connect to the MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)

            # 🔥 IMPORTANT — Start background thread
            self.client.loop_start()

            print(f"[MQTT] Connected to broker at {self.broker_host}:{self.broker_port}")
        except Exception as e:
            print(f"[MQTT] Connection failed: {e}")

    def publish(self, topic: str, message: str):
        """Publish a message to a topic"""
        result = self.client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"[MQTT] Sent `{message}` to topic `{topic}`")
        else:
            print(f"[MQTT] Failed to send message to topic {topic}")
