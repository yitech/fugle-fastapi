from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Fulge Algo API"
    fugle_market_api_key: str
    fugle_trade_config: str

    class Config:
        env_file = ".env"

settings = Settings()