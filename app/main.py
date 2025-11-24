# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import mqtt, token, tweet, devices, ws_devices
from app.database.session import engine
from app.database.base import Base
from app.database.models import Token  # ensures tables are recognized


def create_app() -> FastAPI:
    """
    App factory function — returns a configured FastAPI instance.
    """
    app = FastAPI(
        title="SocialBoost Backend",
        description="MQTT + QR Code + Token Backend",
        version="0.1.0",
    )

    # Create database tables (development only)
    Base.metadata.create_all(bind=engine)

    # Include routers
    app.include_router(mqtt.router, prefix="/mqtt", tags=["MQTT"])
    app.include_router(token.router, prefix="/api", tags=["Token"])  # Token endpoints under /api
    app.include_router(tweet.router, tags=["Tweet"])
    app.include_router(devices.router, prefix="/api/devices", tags=["Devices"])  # Devices endpoints
    app.include_router(ws_devices.router)

    # Health endpoint
    @app.get("/health/ping")
    async def health_check():
        return {"status": "ok", "message": "Backend is running"}

    # ------------------------------
    # CORS middleware for frontend
    # ------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",        # if running frontend locally
            "http://192.168.1.113:3000",    # your server IP for LAN access
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


# Entry point
app = create_app()
