"""
WatchSphere AI v3.0 - Permission Governance Admin Tab Component
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import streamlit as st
import pandas as pd
from backend.services.permission_service import PermissionService


def render_permission_tab() -> None:
    """
    Renders Permission Management tab with interactive RBAC Permission Matrix.
    """
    st.markdown("### 🔐 Role Based Access Control (RBAC) Permission Matrix")

    matrix = PermissionService.get_permission_matrix()
    df_matrix = pd.DataFrame(matrix).T

    st.dataframe(df_matrix, use_container_width=True)
    st.info("💡 Permission matrix modifications update security access control bounds immediately.")
