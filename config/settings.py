from dataclasses import dataclass
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    app_url: str = "http://localhost:8501"
    storage_bucket: str = "grievance-attachments"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be configured.")
    app_url = os.getenv("APP_URL", "http://localhost:8501").strip().rstrip("/")
    return Settings(url, key, app_url)