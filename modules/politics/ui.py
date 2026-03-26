"""Political campaign module UI."""

from __future__ import annotations

import streamlit as st

from prompts import POLITICS_PROMPT_TEMPLATE


def _build_prompt(
    campaign_name: str,
    region: str,
    candidate_name: str,
    campaign_objective: str,
    voter_segment: str,
    key_message: str,
    tone: str,
) -> str:
    return POLITICS_PROMPT_TEMPLATE.format(
        campaign_name=campaign_name.strip(),
        region=region.strip(),
        candidate_name=candidate_name.strip(),
        campaign_objective=campaign_objective.strip(),
        voter_segment=voter_segment.strip(),
        key_message=key_message.strip(),
        tone=tone.strip(),
    )


def render_module() -> None:
    st.title("🗳️ Political Campaign Module")
    st.caption("Fill campaign details to generate an AI-ready communication prompt.")

    with st.form("politics_form", border=False):
        campaign_name = st.text_input("Campaign Name", placeholder="Example: Vision 2026")
        region = st.text_input("Constituency / Region", placeholder="Example: Hyderabad Central")
        candidate_name = st.text_input("Candidate Name", placeholder="Example: A. Kumar")
        campaign_objective = st.selectbox(
            "Campaign Objective",
            options=["Awareness", "Voter Outreach", "Volunteer Recruitment", "Issue Advocacy"],
        )
        voter_segment = st.text_input(
            "Voter Segment",
            placeholder="Example: First-time voters, women voters, youth",
        )
        key_message = st.text_input(
            "Key Promise / Message",
            placeholder="Example: Better jobs, safer neighborhoods, faster public services",
        )
        tone = st.selectbox(
            "Tone",
            options=["Professional", "Inspirational", "Friendly", "Assertive"],
        )
        submitted = st.form_submit_button("Generate Campaign Prompt", use_container_width=True)

    if submitted:
        if not all(
            [
                campaign_name.strip(),
                region.strip(),
                candidate_name.strip(),
                voter_segment.strip(),
                key_message.strip(),
            ]
        ):
            st.error("Please fill all required fields.")
            return

        prompt = _build_prompt(
            campaign_name=campaign_name,
            region=region,
            candidate_name=candidate_name,
            campaign_objective=campaign_objective,
            voter_segment=voter_segment,
            key_message=key_message,
            tone=tone,
        )
        st.success("Prompt generated successfully.")
        st.subheader("Generated Prompt")
        st.code(prompt)
        st.download_button(
            "Download Prompt (.txt)",
            data=prompt,
            file_name=f"{campaign_name.strip().replace(' ', '_').lower()}_politics_prompt.txt",
            mime="text/plain",
        )
