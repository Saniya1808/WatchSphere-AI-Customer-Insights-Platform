"""
WatchSphere AI v3.0 - Power BI Chart Builder Suite
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Any


def render_waterfall_chart(waterfall_data: List[Dict[str, Any]], title: str = "📊 Waterfall Revenue to Net Profit Bridge") -> go.Figure:
    """Renders Power BI style Waterfall Profit Chart."""
    x_labels = [d["label"] for d in waterfall_data]
    y_amounts = [d["amount"] for d in waterfall_data]
    measures = [d["type"] for d in waterfall_data]

    fig = go.Figure(go.Waterfall(
        name="Profit Bridge",
        orientation="v",
        measure=measures,
        x=x_labels,
        textposition="outside",
        text=[f"${abs(val):,.0f}" for val in y_amounts],
        y=y_amounts,
        connector={"line": {"color": "#6366F1"}},
        decreasing={"marker": {"color": "#F43F5E"}},
        increasing={"marker": {"color": "#10B981"}},
        totals={"marker": {"color": "#8B5CF6"}}
    ))
    fig.update_layout(title=title, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
    return fig


def render_sankey_diagram(sankey_data: Dict[str, Any], title: str = "🔀 Supply Chain & Order Fulfillment Sankey Flow") -> go.Figure:
    """Renders Power BI style Sankey Diagram."""
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="#6366F1", width=0.5),
            label=sankey_data["labels"],
            color="#8B5CF6"
        ),
        link=dict(
            source=sankey_data["source"],
            target=sankey_data["target"],
            value=sankey_data["value"],
            color="rgba(99, 102, 241, 0.25)"
        )
    )])
    fig.update_layout(title=title, paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
    return fig


def render_sunburst_chart(df: pd.DataFrame, path_cols: list, value_col: str, title: str = "☀️ Sunburst Category Hierarchy Map") -> go.Figure:
    """Renders Power BI style Sunburst Category Chart."""
    fig = px.sunburst(df, path=path_cols, values=value_col, title=title, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
    return fig


def render_treemap_chart(df: pd.DataFrame, path_cols: list, value_col: str, title: str = "🗺️ Treemap Revenue & Stock Distribution") -> go.Figure:
    """Renders Power BI style Treemap."""
    fig = px.treemap(df, path=path_cols, values=value_col, title=title, color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"})
    return fig


def render_pareto_chart(df_pareto: pd.DataFrame, name_col: str = "name", value_col: str = "revenue", title: str = "🎯 Pareto 80/20 Revenue Contribution Curve") -> go.Figure:
    """Renders Power BI Pareto 80/20 Chart."""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_pareto[name_col], y=df_pareto[value_col], name="Revenue ($)", marker_color="#6366F1"))
    fig.add_trace(go.Scatter(x=df_pareto[name_col], y=df_pareto["cum_pct"], name="Cumulative %", yaxis="y2", mode="lines+markers", line=dict(color="#F43F5E", width=3)))

    fig.update_layout(
        title=title,
        yaxis=dict(title="Revenue ($)"),
        yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC"}
    )
    return fig


def render_gauge_scorecard(value: float, target: float, title: str) -> go.Figure:
    """Renders Gauge Scorecard meter."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={"text": title},
        delta={"reference": target},
        gauge={
            "axis": {"range": [0, target * 1.3]},
            "bar": {"color": "#6366F1"},
            "steps": [
                {"range": [0, target * 0.7], "color": "rgba(244, 63, 94, 0.2)"},
                {"range": [target * 0.7, target], "color": "rgba(245, 158, 11, 0.2)"}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "#F8FAFC"}, height=220)
    return fig
