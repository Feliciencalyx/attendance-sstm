from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    SUPABASE_URL: str = "https://placeholder-project.supabase.co"
    SUPABASE_KEY: str = "placeholder-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    
    CUTOFF_TIME: str = "09:00" # 9:00 AM daily cutoff time for attendance status
    FACE_MATCH_THRESHOLD: float = 0.80 # Cosine similarity threshold for facial vectors
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
