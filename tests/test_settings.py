import pytest

from config import settings


def test_missing_supabase_configuration_is_rejected(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    monkeypatch.setattr(settings, "_streamlit_secret", lambda name: "")
    settings.get_settings.cache_clear()

    with pytest.raises(RuntimeError, match="SUPABASE_URL and SUPABASE_KEY"):
        settings.get_settings()

    settings.get_settings.cache_clear()