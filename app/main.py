# app/main.py

from fastapi import FastAPI
from app.routers import mqtt, token
from app.database.session import engine
from app.database.base import Base
from app.database.models import Token  # ensures tables are recognized
from app.routers import tweet  # add this at the top

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
    app.include_router(token.router, prefix="/token", tags=["Token"])

    # Health endpoint
    @app.get("/health/ping")
    async def health_check():
        return {"status": "ok", "message": "Backend is running"}

    # Inside create_app()
    app.include_router(tweet.router, tags=["Tweet"])


    return app


# Entry point
app = create_app()
