"""Beauty module UI."""

from __future__ import annotations

import streamlit as st

from prompts import BEAUTY_PROMPT_TEMPLATE


def _build_prompt(
    brand_name: str,
    city_area: str,
    business_type: str,
    primary_service: str,
    target_audience: str,
    current_offer: str,
    tone: str,
) -> str:
    return BEAUTY_PROMPT_TEMPLATE.format(
        brand_name=brand_name.strip(),
        city_area=city_area.strip(),
        business_type=business_type.strip(),
        primary_service=primary_service.strip(),
        target_audience=target_audience.strip(),
        current_offer=current_offer.strip(),
        tone=tone.strip(),
    )


def render_module() -> None:
    st.title("💄 Beauty Marketing Module")
    st.caption("Provide your salon/clinic details to generate a ready AI prompt.")

    with st.form("beauty_form", border=False):
        brand_name = st.text_input("Brand Name", placeholder="Example: GlowCraft Studio")
        city_area = st.text_input("City / Area Focus", placeholder="Example: Hyderabad - Jubilee Hills")
        business_type = st.selectbox(
            "Business Type",
            options=["Salon", "Skin Clinic", "Bridal Studio", "Nail Studio", "Beauty Spa"],
        )
        primary_service = st.text_input(
            "Primary Service",
            placeholder="Example: Bridal makeup, skin treatments, hair color",
        )
        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: Women 22-40, working professionals",
        )
        current_offer = st.text_input(
            "Current Offer",
            placeholder="Example: 30% off on first facial session",
        )
        tone = st.selectbox(
            "Tone",
            options=["Premium", "Friendly", "Elegant", "Aggressive Marketing"],
        )
        submitted = st.form_submit_button("Generate Beauty Prompt", use_container_width=True)

    if submitted:
        if not all(
            [
                brand_name.strip(),
                city_area.strip(),
                primary_service.strip(),
                target_audience.strip(),
                current_offer.strip(),
            ]
        ):
            st.error("Please fill all required fields.")
            return

        prompt = _build_prompt(
            brand_name=brand_name,
            city_area=city_area,
            business_type=business_type,
            primary_service=primary_service,
            target_audience=target_audience,
            current_offer=current_offer,
            tone=tone,
        )
        st.success("Prompt generated successfully.")
        st.subheader("Generated Prompt")
        st.code(prompt)
        st.download_button(
            "Download Prompt (.txt)",
            data=prompt,
            file_name=f"{brand_name.strip().replace(' ', '_').lower()}_beauty_prompt.txt",
            mime="text/plain",
        )
