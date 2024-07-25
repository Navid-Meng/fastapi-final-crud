from pydantic_settings import BaseSettings #type: ignore

class Settings(BaseSettings):
    mysql_database_url: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()