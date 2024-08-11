from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Fugle FastAPI"
    fugle_market_api_key: str
    fugle_trade_config: str
    api_secret: Optional[str] = None
    domain: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()  # type: ignore