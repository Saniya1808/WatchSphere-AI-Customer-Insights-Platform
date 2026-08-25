"""
WatchSphere AI v3.0 - Ultra-Premium Landing & Authentication Page
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
from frontend.utils.auth_client import AuthClient
from frontend.utils.session import SessionManager
from frontend.utils.css_loader import load_css
from config.constants import APP_AUTHOR, INTERNSHIP_CREDIT


def render_landing_page() -> None:
    """
    Renders the Phase 2 ultra-premium landing page with hero highlights and tabbed authentication card.
    """
    load_css()

    col_hero, col_auth = st.columns([1.2, 1], gap="large")

    # ================= LEFT HERO SIDE =================
    with col_hero:
        st.markdown(
            """
            <div class="ws-floating-badge">
                ⚡ Enterprise AI Powered Platform • Version 3.0
            </div>
            <h1 class="ws-hero-title">WatchSphere AI</h1>
            <p style="font-size: 1.25rem; font-weight: 600; color: var(--accent-indigo); margin-bottom: 20px;">
                Enterprise AI Powered Customer Analytics Platform
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style="font-size: 1rem; color: var(--text-sub); line-height: 1.6; margin-bottom: 28px;">
                Empowering global enterprises with real-time customer behavior intelligence, predictive analytics forecasting, and executive business intelligence dashboards.
            </p>
            """,
            unsafe_allow_html=True
        )

        # Feature Highlights List
        st.markdown("### ✨ Feature Highlights")
        features = [
            ("🤖", "AI Analytics", "Real-time behavior scoring & sentiment clustering"),
            ("📊", "Executive Dashboard", "High-throughput metric visualization shell"),
            ("🔮", "Forecasting", "Predictive churn & revenue trajectory modeling"),
            ("💡", "Recommendations", "Automated customer retention strategy engine"),
            ("🎯", "Customer Intelligence", "Unified 360-degree customer profile analytics")
        ]

        for icon, title, desc in features:
            st.markdown(
                f"""
                <div class="ws-feature-item">
                    <div class="ws-feature-icon">{icon}</div>
                    <div>
                        <strong style="color: var(--text-main);">{title}</strong> — <span style="font-size: 0.875rem; color: var(--text-sub);">{desc}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Professional Illustration Placeholder
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="ws-glass-card" style="padding: 20px; text-align: center; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));">
                <svg width="100%" height="90" viewBox="0 0 400 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 80 Q 100 20, 200 60 T 390 10" stroke="url(#paint0_linear)" stroke-width="4" stroke-linecap="round" fill="none"/>
                    <circle cx="200" cy="60" r="6" fill="#6366F1"/>
                    <circle cx="390" cy="10" r="6" fill="#EC4899"/>
                    <defs>
                        <linearGradient id="paint0_linear" x1="0" y1="0" x2="400" y2="0" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#6366F1"/>
                            <stop offset="0.5" stop-color="#8B5CF6"/>
                            <stop offset="1" stop-color="#EC4899"/>
                        </linearGradient>
                    </defs>
                </svg>
                <div style="font-size: 0.8rem; color: var(--text-sub); font-weight: 500;">
                    📈 High-Performance Predictive Data Stream Architecture
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Left Hero Footer
        st.markdown(
            f"""
            <div style="margin-top: 30px; font-size: 0.85rem; color: var(--text-muted); border-top: 1px solid var(--border-glass); padding-top: 16px;">
                <strong>{APP_AUTHOR}</strong> • WatchSphere AI Version 3.0 • <strong>{INTERNSHIP_CREDIT}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================= RIGHT AUTH TABBED CARD =================
    with col_auth:
        st.markdown(
            """
            <div class="ws-glass-card" style="border-top: 4px solid var(--accent-indigo);">
                <h2 style="font-family: var(--font-heading); margin-top: 0; font-size: 1.6rem; color: var(--text-main);">
                    🔐 Account Authentication
                </h2>
                <p style="font-size: 0.875rem; color: var(--text-sub); margin-bottom: 20px;">
                    Select your portal role and sign in with your JWT credentials.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        tab_vendor, tab_admin = st.tabs(["🏬 Vendor Login", "👑 Admin Login"])

        # ------------ VENDOR LOGIN TAB ------------
        with tab_vendor:
            st.caption("Sign in to Vendor Portal")
            v_company = st.text_input("Vendor Company Name", value="Acme Watch Co.", key="v_company_input")
            v_email = st.text_input("Vendor Email", value="vendor@watchsphere.ai", key="v_email_input")
            v_password = st.text_input("Password", value="Vendor@123", type="password", key="v_password_input")
            
            col_v_rem, col_v_fg = st.columns([1, 1])
            with col_v_rem:
                v_remember = st.checkbox("Remember Me", value=True, key="v_remember")
            with col_v_fg:
                st.markdown("<div style='text-align: right;'><a href='#' style='color: #6366F1; font-size: 0.85rem;'>Forgot Password?</a></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Sign In as Vendor", use_container_width=True, key="v_login_btn", type="primary"):
                if not v_email or not v_password:
                    st.error("Please enter email and password.")
                else:
                    success, msg, profile, token = AuthClient.login(v_email, v_password, v_company)
                    if success:
                        SessionManager.set_user_session(profile, token)
                        st.success("Vendor Login Successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(msg)

        # ------------ ADMIN LOGIN TAB ------------
        with tab_admin:
            st.caption("Sign in to Administrator Portal")
            a_email = st.text_input("Admin Email", value="admin@watchsphere.ai", key="a_email_input")
            a_password = st.text_input("Password", value="Admin@123", type="password", key="a_password_input")
            
            col_a_rem, col_a_fg = st.columns([1, 1])
            with col_a_rem:
                a_remember = st.checkbox("Remember Me", value=True, key="a_remember")
            with col_a_fg:
                st.markdown("<div style='text-align: right;'><a href='#' style='color: #6366F1; font-size: 0.85rem;'>Forgot Password?</a></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("👑 Sign In as Admin", use_container_width=True, key="a_login_btn", type="primary"):
                if not a_email or not a_password:
                    st.error("Please enter email and password.")
                else:
                    success, msg, profile, token = AuthClient.login(a_email, a_password)
                    if success:
                        SessionManager.set_user_session(profile, token)
                        st.success("Admin Login Successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(msg)
