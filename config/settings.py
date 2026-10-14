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


def _streamlit_secret(name: str) -> str:
    try:
        import streamlit as st

        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    url = os.getenv("SUPABASE_URL", "").strip() or _streamlit_secret("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY", "").strip() or _streamlit_secret("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be configured.")
    app_url = (os.getenv("APP_URL", "").strip() or _streamlit_secret("APP_URL") or "http://localhost:8501").rstrip("/")
    return Settings(url, key, app_url)