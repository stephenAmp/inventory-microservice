from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str

    class Config:
        env_file = '.env'

settings = Settings()