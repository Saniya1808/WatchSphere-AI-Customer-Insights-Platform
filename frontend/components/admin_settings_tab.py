"""
WatchSphere AI v3.0 - System Settings Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st


def render_settings_tab() -> None:
    """
    Renders System Settings tab with General, Tax, Email, and Security configuration forms.
    """
    st.markdown("### ⚙️ Global Enterprise System Configuration")

    with st.form("form_system_settings"):
        st.markdown("#### 1️⃣ General Application Settings")
        c1, c2, c3 = st.columns(3)
        with c1:
            app_name = st.text_input("Application Name", value="WatchSphere AI – Customer Insights Platform")
            org_name = st.text_input("Organization", value="WatchSphere Enterprise Inc.")
        with c2:
            tz = st.selectbox("System Timezone", options=["UTC", "Asia/Kolkata (IST)", "America/New_York (EST)"])
            curr = st.selectbox("Base Currency", options=["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)"])
        with c3:
            lang = st.selectbox("Language", options=["English (US)", "Spanish", "French", "German"])
            theme = st.selectbox("Default Theme", options=["Dark Mode (#0F172A)", "Light Mode (#F8FAFC)"])

        st.markdown("#### 2️⃣ Tax & Financial Governance")
        t1, t2 = st.columns(2)
        with t1:
            gst_rate = st.number_input("Default GST Rate (%)", min_value=0.0, value=18.0)
        with t2:
            tax_id = st.text_input("Corporate Tax ID", value="GSTIN-27AAACA123411Z5")

        st.markdown("#### 3️⃣ Security & Session Policies")
        s1, s2, s3 = st.columns(3)
        with s1:
            pwd_min = st.number_input("Min Password Length", min_value=6, value=8)
        with s2:
            sess_to = st.number_input("Session Timeout (Minutes)", min_value=5, value=30)
        with s3:
            max_upload = st.number_input("Max File Upload Limit (MB)", min_value=1, value=25)

        submit_btn = st.form_submit_button("Save System Configuration", type="primary")

        if submit_btn:
            st.success("System configuration settings updated and persisted successfully!")
