"""Wasted food: headline € and grid by period with trends."""

from dash import html

WASTE_EUR = 1840
WASTE_EUR_DELTA = -5.2

WASTE_KG = {
    "DAY": {"kg": 42, "delta": 2.1},
    "MONTH": {"kg": 1180, "delta": -3.4},
    "SEASONAL": {"kg": 3400, "delta": 1.0},
    "YEAR": {"kg": 13200, "delta": -0.8},
}


def _arrow(delta: float) -> html.Span:
    if delta > 0.05:
        return html.Span(" ▲", className="trend-up")
    if delta < -0.05:
        return html.Span(" ▼", className="trend-down")
    return html.Span(" ▬", className="trend-flat")


def create_waste_widget():
    grid = html.Div(
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "10px",
            "marginTop": "14px",
        },
        children=[
            html.Div(
                className="panel",
                style={"padding": "10px 12px", "background": "var(--surface-2)"},
                children=[
                    html.Div(k, style={"fontSize": "10px", "color": "var(--muted)", "letterSpacing": "0.08em"}),
                    html.Div(
                        [
                            html.Span(f"{WASTE_KG[k]['kg']:,} kg", style={"fontWeight": "700", "fontSize": "15px"}),
                            html.Span(
                                f" {WASTE_KG[k]['delta']:+.1f}%",
                                style={"fontSize": "11px", "color": "var(--muted)"},
                            ),
                            _arrow(WASTE_KG[k]["delta"]),
                        ],
                        style={"marginTop": "6px"},
                    ),
                ],
            )
            for k in ["DAY", "MONTH", "SEASONAL", "YEAR"]
        ],
    )

    headline = html.Div(
        style={"display": "flex", "alignItems": "baseline", "gap": "10px", "flexWrap": "wrap"},
        children=[
            html.Span(f"€ {WASTE_EUR:,.0f}", style={"fontSize": "30px", "fontWeight": "800"}),
            html.Span(
                [
                    html.Span(f"vs last month {WASTE_EUR_DELTA:+.1f}%", style={"color": "var(--muted)", "fontSize": "13px"}),
                    _arrow(WASTE_EUR_DELTA),
                ]
            ),
        ],
    )

    return html.Div(
        className="panel",
        children=[
            html.H3("Wasted food", className="panel-title"),
            headline,
            grid,
        ],
    )
