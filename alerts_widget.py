"""ALERTS panel: urgency-colored indicators and due dates."""

from datetime import date, timedelta

from dash import html

URGENCY = {
    "critical": {"color": "var(--red)", "label": "Critical"},
    "warning": {"color": "var(--yellow)", "label": "Warning"},
    "ok": {"color": "var(--green)", "label": "OK"},
}


def _mock_alerts():
    today = date.today()
    return [
        {
            "urgency": "critical",
            "title": "Vendor price change",
            "due": today + timedelta(days=1),
            "body": "Produce basket quote expires; confirm locked pricing with supplier.",
        },
        {
            "urgency": "warning",
            "title": "Par level drift",
            "due": today + timedelta(days=3),
            "body": "Dry storage is 18% below target par for banquet week.",
        },
        {
            "urgency": "warning",
            "title": "Menu margin check",
            "due": today + timedelta(days=5),
            "body": "Seafood platter food cost crossed 32% — review portion or pricing.",
        },
        {
            "urgency": "ok",
            "title": "Inventory audit",
            "due": today + timedelta(days=14),
            "body": "Scheduled full count for Sunday close; prep count sheets.",
        },
    ]


def create_alerts_widget():
    rows = []
    for a in _mock_alerts():
        u = URGENCY[a["urgency"]]
        rows.append(
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "14px 1fr",
                    "gap": "10px",
                    "padding": "10px 0",
                    "borderBottom": "1px solid var(--border)",
                },
                children=[
                    html.Div(
                        style={
                            "width": "10px",
                            "height": "10px",
                            "borderRadius": "50%",
                            "background": u["color"],
                            "marginTop": "4px",
                            "boxShadow": f"0 0 0 2px color-mix(in srgb, {u['color']} 35%, transparent)",
                        },
                        title=u["label"],
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "baseline",
                                    "gap": "8px",
                                },
                                children=[
                                    html.Span(
                                        a["title"],
                                        style={"fontWeight": "600", "fontSize": "13px"},
                                    ),
                                    html.Span(
                                        a["due"].strftime("%d %b %Y"),
                                        style={"fontSize": "11px", "color": "var(--muted)"},
                                    ),
                                ],
                            ),
                            html.Div(
                                a["body"],
                                style={
                                    "fontSize": "12px",
                                    "color": "var(--muted)",
                                    "marginTop": "4px",
                                    "lineHeight": 1.45,
                                },
                            ),
                        ],
                    ),
                ],
            )
        )

    return html.Div(
        className="panel",
        style={"minHeight": "280px"},
        children=[
            html.H3("Alerts", className="panel-title"),
            html.Div(children=rows),
        ],
    )
