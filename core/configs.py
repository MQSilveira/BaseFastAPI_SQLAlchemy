from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://teste:123456@192.168.0.53:5439/postgres'
    DBBaseModel = declarative_base()
    
    class Config:
        case_sesitive = True

settings = Settings()


