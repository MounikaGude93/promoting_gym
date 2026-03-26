"""Supabase authentication helpers for Streamlit app."""

from __future__ import annotations

import streamlit as st
from supabase import Client, create_client


def init_supabase() -> Client:
    """Initialize and return Supabase client from Streamlit secrets."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def sign_up(email: str, password: str):
    """Create a Supabase auth user and persist session user."""
    supabase = init_supabase()
    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
            "options": {"data": {"plan": "free"}},
        }
    )
    st.session_state["user"] = response.user
    return response


def sign_in(email: str, password: str):
    """Sign in with Supabase and persist session user."""
    supabase = init_supabase()
    response = supabase.auth.sign_in_with_password(
        {"email": email, "password": password}
    )
    st.session_state["user"] = response.user
    return response


def sign_out() -> None:
    """Sign out current user and clear session user."""
    supabase = init_supabase()
    supabase.auth.sign_out()
    st.session_state["user"] = None


def get_user_plan(email: str) -> str:
    """Read plan from current session user metadata, defaulting to free."""
    _ = email  # Signature kept for forward compatibility with DB lookups.
    user = st.session_state.get("user")
    if not user:
        return "free"

    metadata = getattr(user, "user_metadata", None) or {}
    plan = metadata.get("plan", "free")
    if plan not in {"free", "pro"}:
        return "free"
    return plan
