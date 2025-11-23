from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SocialBoost Backend"
    DEBUG: bool = True

    # Add more settigs later; database URL, MQTT host, API keys, etc.

    class Config:
        env_file = ".env"
