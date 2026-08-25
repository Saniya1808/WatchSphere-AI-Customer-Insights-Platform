"""
WatchSphere AI v3.0 - Components Package Export
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from frontend.components.header import render_header
from frontend.components.footer import render_footer
from frontend.components.cards import render_metric_card, render_architecture_card
from frontend.components.alerts import render_alert

__all__ = [
    "render_header",
    "render_footer",
    "render_metric_card",
    "render_architecture_card",
    "render_alert",
]
