"""Real estate module UI."""

from __future__ import annotations

import streamlit as st

from prompts import REAL_ESTATE_PROMPT_TEMPLATE


def _build_prompt(
    brand_name: str,
    city_area: str,
    property_type: str,
    target_buyer: str,
    current_offer: str,
    tone: str,
) -> str:
    return REAL_ESTATE_PROMPT_TEMPLATE.format(
        brand_name=brand_name.strip(),
        city_area=city_area.strip(),
        property_type=property_type.strip(),
        target_buyer=target_buyer.strip(),
        current_offer=current_offer.strip(),
        tone=tone.strip(),
    )


def render_module() -> None:
    st.title("🏡 Real Estate Marketing Module")
    st.caption("Tell us your project details and generate a ready AI prompt.")

    with st.form("real_estate_form", border=False):
        brand_name = st.text_input("Brand Name", placeholder="Example: Urban Nest Realty")
        city_area = st.text_input("City / Area Focus", placeholder="Example: Hyderabad - Gachibowli")
        property_type = st.selectbox(
            "Property Type",
            options=["Residential", "Commercial", "Plots", "Luxury Homes", "Mixed Portfolio"],
        )
        target_buyer = st.text_input(
            "Target Buyer Segment",
            placeholder="Example: IT professionals, first-time buyers",
        )
        current_offer = st.text_input(
            "Current Offer",
            placeholder="Example: No brokerage + free site visit",
        )
        tone = st.selectbox(
            "Tone",
            options=["Professional", "Premium", "Friendly", "Aggressive Marketing"],
        )
        submitted = st.form_submit_button("Generate Real Estate Prompt", use_container_width=True)

    if submitted:
        if not all([brand_name.strip(), city_area.strip(), target_buyer.strip(), current_offer.strip()]):
            st.error("Please fill all required fields.")
            return

        prompt = _build_prompt(
            brand_name=brand_name,
            city_area=city_area,
            property_type=property_type,
            target_buyer=target_buyer,
            current_offer=current_offer,
            tone=tone,
        )
        st.success("Prompt generated successfully.")
        st.subheader("Generated Prompt")
        st.code(prompt)
        st.download_button(
            "Download Prompt (.txt)",
            data=prompt,
            file_name=f"{brand_name.strip().replace(' ', '_').lower()}_real_estate_prompt.txt",
            mime="text/plain",
        )
