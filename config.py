import os

class Settings:
    SERVICE_NAME: str = "aws-learning-service-three"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    PORT: int = int(os.getenv("PORT", "8003"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
