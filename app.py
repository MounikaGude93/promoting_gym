"""Multi-industry AI marketing platform entrypoint."""

from __future__ import annotations

import re

import streamlit as st
from dotenv import load_dotenv

from auth import get_user_plan, sign_in, sign_out, sign_up
from payments import render_upgrade_page

INDUSTRIES = ["Gym", "Real Estate", "Beauty", "Political Campaign"]


def inject_platform_css() -> None:
    """Apply premium app-wide styles."""
    st.markdown(
        """
        <style>
            .main {
                background: radial-gradient(circle at top left, #111b36 0%, #0a1022 55%, #070b17 100%);
                color: #e7ecff;
            }
            .platform-hero {
                border: 1px solid rgba(255,255,255,0.14);
                border-radius: 18px;
                padding: 1.15rem 1.35rem;
                background: linear-gradient(135deg, rgba(99,102,241,0.30), rgba(16,185,129,0.22));
                margin-bottom: 1rem;
            }
            .plan-chip {
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 12px;
                padding: 0.8rem 1rem;
                background: rgba(255,255,255,0.05);
                margin-bottom: 0.8rem;
            }
            .top-nav {
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 12px;
                padding: 0.55rem 0.85rem;
                background: rgba(255,255,255,0.04);
                margin-bottom: 0.9rem;
            }
            .auth-card {
                border: 1px solid rgba(255,255,255,0.14);
                border-radius: 16px;
                padding: 1rem 1.1rem;
                background: rgba(255,255,255,0.04);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def ensure_supabase_secrets() -> None:
    """Show setup hint when required Supabase secrets are missing."""
    missing_keys = []
    try:
        secrets = st.secrets
        if not secrets.get("SUPABASE_URL"):
            missing_keys.append("SUPABASE_URL")
        if not secrets.get("SUPABASE_KEY"):
            missing_keys.append("SUPABASE_KEY")
    except Exception:
        missing_keys = ["SUPABASE_URL", "SUPABASE_KEY"]

    if missing_keys:
        st.error(
            "Supabase is not configured. Add these keys in Streamlit secrets: "
            + ", ".join(missing_keys)
        )
        st.code(
            'SUPABASE_URL = "https://your-project-id.supabase.co"\n'
            'SUPABASE_KEY = "your-anon-or-publishable-key"',
            language="toml",
        )
        st.stop()


def render_auth_page() -> None:
    """Render auth UI and stop app until user signs in."""
    if st.session_state.get("user"):
        return

    def _friendly_auth_error(exc: Exception) -> str:
        text = str(exc)
        if "after" in text.lower() and "seconds" in text.lower():
            match = re.search(r"after\s+(\d+)\s+seconds", text, flags=re.IGNORECASE)
            if match:
                return (
                    f"For security, please wait {match.group(1)} seconds and try again."
                )
            return "For security, please wait about a minute and try again."
        if "invalid login credentials" in text.lower():
            return "Invalid email or password."
        if "rate limit" in text.lower():
            return "Rate limit reached. Please wait and retry."
        return "Authentication failed. Please try again."

    inject_platform_css()
    st.markdown(
        """
        <div class="platform-hero">
            <h1 style="margin:0;">AI Marketing Assistant Platform</h1>
            <p style="margin:0.45rem 0 0 0;">
                One login. One subscription. Multiple industries.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.title("Sign in to continue")
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", use_container_width=True):
            try:
                sign_in(login_email, login_password)
                st.success("Logged in successfully.")
                st.rerun()
            except Exception as exc:
                st.error(_friendly_auth_error(exc))

    with signup_tab:
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Create Account", use_container_width=True):
            try:
                sign_up(signup_email, signup_password)
                st.success("Account created. Please check verification email if enabled.")
                st.rerun()
            except Exception as exc:
                st.error(_friendly_auth_error(exc))

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


def render_locked_industry() -> None:
    """Show locked state for premium industries."""
    st.warning("Upgrade to Pro to access this industry 🚀")
    st.button("Upgrade to Pro ₹999/month", use_container_width=True)
    render_upgrade_page()


def main() -> None:
    load_dotenv()
    st.set_page_config(
        page_title="AI Marketing Assistant Platform",
        page_icon="🚀",
        layout="wide",
    )
    inject_platform_css()
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("industry", "Gym")

    ensure_supabase_secrets()
    render_auth_page()

    user = st.session_state.get("user")
    user_email = user.email if user else ""
    plan = get_user_plan(user_email)

    st.markdown(
        """
        <div class="platform-hero">
            <h1 style="margin:0;">AI Marketing Assistant Platform</h1>
            <p style="margin:0.45rem 0 0 0;">Generate social media content for multiple industries.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_meta, right_meta = st.columns([4, 1])
    with left_meta:
        st.markdown(
            f"""
            <div class="top-nav">
                <strong>Logged in:</strong> {user_email} &nbsp; | &nbsp;
                <strong>Plan:</strong> {plan.title()}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right_meta:
        if st.button("Sign Out", use_container_width=True):
            sign_out()
            st.rerun()

    st.markdown(
        f"""
        <div class="plan-chip">
            <strong>{plan.title()} Plan Active</strong><br>
            Free: Gym only. Pro unlocks all industries.
        </div>
        """,
        unsafe_allow_html=True,
    )
    tab_gym, tab_re, tab_beauty, tab_pol = st.tabs(INDUSTRIES)

    with tab_gym:
        st.session_state["industry"] = "Gym"
        import modules.gym.ui as gym_ui

        gym_ui.render_module()

    with tab_re:
        st.session_state["industry"] = "Real Estate"
        if plan == "free":
            render_locked_industry()
        else:
            import modules.real_estate.ui as re_ui

            re_ui.render_module()

    with tab_beauty:
        st.session_state["industry"] = "Beauty"
        if plan == "free":
            render_locked_industry()
        else:
            import modules.beauty.ui as beauty_ui

            beauty_ui.render_module()

    with tab_pol:
        st.session_state["industry"] = "Political Campaign"
        if plan == "free":
            render_locked_industry()
        else:
            import modules.politics.ui as politics_ui

            politics_ui.render_module()


if __name__ == "__main__":
    main()
