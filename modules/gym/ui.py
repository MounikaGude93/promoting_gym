"""Gym industry module UI."""

from __future__ import annotations

import io
from typing import Optional

import streamlit as st

from content_bank import TARGET_CONTENT
from content_store import get_next_post, get_usage_progress, reset_target_usage

TELANGANA_LOCATIONS = [
    "Hyderabad",
    "Secunderabad",
    "Gachibowli",
    "Madhapur",
    "Kukatpally",
    "Kondapur",
    "Miyapur",
    "Nizampet",
    "Manikonda",
    "Jubilee Hills",
    "Banjara Hills",
    "Begumpet",
    "Hitech City",
    "Warangal",
    "Karimnagar",
    "Nizamabad",
    "Khammam",
    "Nalgonda",
    "Siddipet",
]


def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
            .main {
                background: linear-gradient(180deg, #0b1020 0%, #11192f 100%);
                color: #e7ecff;
            }
            .hero-card {
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 16px;
                padding: 1.2rem 1.4rem;
                background: linear-gradient(135deg, rgba(99,102,241,0.20), rgba(34,197,94,0.18));
                margin-bottom: 1rem;
            }
            .kpi-card {
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 14px;
                padding: 0.9rem 1rem;
                background: rgba(255,255,255,0.04);
                margin-bottom: 0.7rem;
            }
            .section-title {
                font-size: 1.05rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }
            .stDownloadButton > button {
                width: 100%;
                border-radius: 10px;
                font-weight: 600;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_post_output(
    gym_name: str,
    city: str,
    audience: str,
    tone: str,
    region_focus: str,
    post: dict[str, str | int],
) -> str:
    return (
        f"### {gym_name} | {post['target'].replace('_', ' ').title()} - Day {post['day']}\n\n"
        f"**City:** {city}\n\n"
        f"**Target Audience:** {audience}\n\n"
        f"**Tone:** {tone}\n\n"
        f"**Location Focus:** {region_focus}\n\n"
        f"**Post Caption:**\n{post['caption']}\n\n"
        f"**Suggested Image Idea:**\n{post['image_idea']}\n\n"
        f"**Hashtags:**\n{post['hashtags']}\n"
    )


def validate_inputs(gym_name: str, city: str, audience: str) -> Optional[str]:
    if not gym_name.strip():
        return "Please enter a gym name."
    if not city.strip():
        return "Please enter a city."
    if not audience.strip():
        return "Please enter a target audience."
    return None


def render_module() -> None:
    """Render gym generator module."""
    inject_custom_css()
    st.markdown(
        """
        <div class="hero-card">
            <h2 style="margin:0;">AI Social Media Generator for Gyms</h2>
            <p style="margin:0.5rem 0 0 0;">
                Create 30 days of high-converting Instagram content tailored for
                Hyderabad and Telangana-based gyms.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.45, 1], gap="large")

    with left_col:
        with st.form("gym_generator_form", border=False):
            st.markdown('<div class="section-title">Gym Profile</div>', unsafe_allow_html=True)
            gym_name = st.text_input("Gym Name", placeholder="Example: Iron Pulse Fitness")
            audience = st.text_input(
                "Target Audience",
                placeholder="Example: Working professionals aged 22-40",
            )
            city = st.selectbox("City", options=TELANGANA_LOCATIONS, index=0)
            content_target = st.selectbox(
                "Content Target",
                options=list(TARGET_CONTENT.keys()),
                format_func=lambda t: t.replace("_", " ").title(),
            )
            tone = st.selectbox(
                "Tone",
                options=["Motivational", "Friendly", "Professional", "Energetic"],
            )
            region_focus = st.selectbox(
                "Location Focus",
                options=["Hyderabad", "Telangana", "Hyderabad + Telangana"],
                index=2,
            )
            submitted = st.form_submit_button(
                "Generate Next Post",
                use_container_width=True,
            )

    with right_col:
        st.markdown('<div class="section-title">Why This Works</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="kpi-card"><strong>Local-first strategy</strong><br>
            Content is tuned for Hyderabad/Telangana audience behavior.</div>
            <div class="kpi-card"><strong>30 days instantly</strong><br>
            Go from idea to monthly calendar in one click.</div>
            <div class="kpi-card"><strong>Post-ready format</strong><br>
            Captions, image ideas, and hashtags included.</div>
            """,
            unsafe_allow_html=True,
        )
        used_count, total_count = get_usage_progress(content_target)
        st.info(
            f"Progress for {content_target.replace('_', ' ').title()}: {used_count}/{total_count} used"
        )
        if st.button("Reset This Target Sequence", use_container_width=True):
            reset_target_usage(content_target)
            st.success("Target sequence reset. Day 1 will be served on next click.")

    if submitted:
        error_message = validate_inputs(gym_name, city, audience)
        if error_message:
            st.error(error_message)
            return

        try:
            with st.spinner("Fetching next post from your content bank..."):
                post = get_next_post(content_target)
                if post is None:
                    st.warning(
                        "All 10 posts are already used for this target. "
                        "Click 'Reset This Target Sequence' to start again."
                    )
                    return
                result = format_post_output(
                    gym_name=gym_name,
                    city=city,
                    audience=audience,
                    tone=tone,
                    region_focus=region_focus,
                    post=post,
                )
        except Exception as exc:
            st.error(
                "Something went wrong while loading the next post. Please try again."
            )
            st.exception(exc)
            return

        st.success("Next post is ready.")
        result_col, meta_col = st.columns([1.6, 1], gap="large")
        with result_col:
            st.subheader("Generated Post")
            st.markdown(result)
        with meta_col:
            st.markdown("### Campaign Snapshot")
            st.markdown(f"- **Gym:** {gym_name}")
            st.markdown(f"- **City:** {city}")
            st.markdown(f"- **Audience:** {audience}")
            st.markdown(f"- **Target:** {content_target.replace('_', ' ').title()}")
            st.markdown(f"- **Tone:** {tone}")
            st.markdown(f"- **Focus:** {region_focus}")
            used_count, total_count = get_usage_progress(content_target)
            st.markdown(f"- **Used:** {used_count}/{total_count}")

        file_buffer = io.StringIO()
        file_buffer.write(result)
        file_name = f"{gym_name.strip().replace(' ', '_').lower()}_30_day_content_calendar.txt"
        st.download_button(
            label="Download as Text File",
            data=file_buffer.getvalue(),
            file_name=file_name,
            mime="text/plain",
        )
