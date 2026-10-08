from datetime import datetime
from typing import Any

import streamlit as st

from utils.constants import STATUS_CONFIG


def inject_styles() -> None:
    st.markdown("""
    <style>
    :root { --navy:#102a43; --blue:#1769aa; --ink:#243b53; --muted:#627d98; --paper:#f6f8fb; --line:#d9e2ec; }
    .stApp { background:var(--paper); color:var(--ink); }
    [data-testid="stMain"] [data-testid="stWidgetLabel"],
    [data-testid="stMain"] [data-testid="stWidgetLabel"] p,
    [data-testid="stMain"] [data-testid="stWidgetLabel"] label,
    [data-testid="stMain"] label { color:var(--ink) !important; }
    [data-testid="stMain"] input, [data-testid="stMain"] textarea { color:var(--ink) !important; }
    [data-testid="stMain"] [data-testid="stTextInputRootElement"],
    [data-testid="stMain"] [data-testid="stTextAreaRootElement"],
    [data-testid="stMain"] [data-testid="stNumberInputRootElement"],
    [data-testid="stMain"] [data-baseweb="select"] > div { background:#ffffff !important; color:var(--ink) !important; border-color:var(--line) !important; }
    [data-testid="stMain"] input::placeholder, [data-testid="stMain"] textarea::placeholder { color:var(--muted) !important; opacity:1; }
    [data-testid="stMain"] [data-baseweb="tab"], [data-testid="stMain"] [data-baseweb="tab"] p { color:var(--ink) !important; }
    [data-testid="stSidebar"] { background:#102a43; }
    [data-testid="stSidebar"] * { color:#f0f4f8; }
    .portal-kicker { color:#1769aa; font-weight:700; letter-spacing:.08em; text-transform:uppercase; font-size:.75rem; }
    .portal-title { color:#102a43; font-size:2.25rem; line-height:1.1; font-weight:800; margin:0 0 .5rem; }
    .card { background:white; border:1px solid #d9e2ec; border-radius:8px; padding:1.15rem; box-shadow:0 4px 16px rgba(16,42,67,.05); }
    .metric-label { color:#627d98; font-size:.8rem; text-transform:uppercase; letter-spacing:.05em; }
    .metric-value { color:#102a43; font-size:1.8rem; font-weight:800; margin-top:.25rem; }
    .status { display:inline-block; border-radius:999px; padding:.2rem .65rem; font-size:.78rem; font-weight:700; }
    </style>
    """, unsafe_allow_html=True)


def page_header(kicker: str, title: str, description: str = "") -> None:
    st.markdown(f'<div class="portal-kicker">{kicker}</div><h1 class="portal-title">{title}</h1>', unsafe_allow_html=True)
    if description:
        st.caption(description)


def status_badge(status: str) -> None:
    config = STATUS_CONFIG.get(status, {"label": status, "icon": "", "color": "#475569"})
    st.markdown(f'<span class="status" style="background:{config["color"]}18;color:{config["color"]}">{config["icon"]} {config["label"]}</span>', unsafe_allow_html=True)


def format_date(value: Any) -> str:
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        return str(value)