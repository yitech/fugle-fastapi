from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Fulge Algo API"

    class Config:
        env_file = ".env"

settings = Settings()