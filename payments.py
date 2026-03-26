"""Payment placeholder UI."""

import streamlit as st


def render_upgrade_page(key_prefix: str = "upgrade") -> None:
    """Render upgrade information and CTA placeholder."""
    st.markdown("## Upgrade Your Plan")
    st.caption("Razorpay integration placeholder for V1.")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### Free Plan")
        st.markdown("- Gym module")
        st.markdown("- Limited usage")
    with col2:
        st.markdown("### Pro Plan ₹999/month")
        st.markdown("- All industries")
        st.markdown("- Unlimited usage")
        st.markdown("- Future features")

    payment_link = st.secrets.get("RAZORPAY_PAYMENT_LINK", "")
    if payment_link:
        st.link_button(
            "Upgrade with Razorpay",
            payment_link,
            use_container_width=True,
            key=f"{key_prefix}_razorpay_link",
        )
    else:
        st.button(
            "Upgrade with Razorpay (Coming Soon)",
            use_container_width=True,
            key=f"{key_prefix}_razorpay_button",
        )
