"""Top bar: logo placeholder, hotel name, branding, user menu, hotel switcher."""

from dash import dcc, html

HOTELS = [
    {"id": "h1", "label": "Grand Riviera Resort"},
    {"id": "h2", "label": "Harbor View Suites"},
    {"id": "h3", "label": "Alpine Lodge & Spa"},
    {"id": "h4", "label": "City Central Hotel"},
]


def create_header():
    return html.Div(
        className="panel",
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "padding": "10px 20px",
            "marginBottom": "16px",
            "borderRadius": "12px",
        },
        children=[
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "14px"},
                children=[
                    html.Div(
                        "Logo",
                        style={
                            "width": "44px",
                            "height": "44px",
                            "borderRadius": "8px",
                            "border": "1px dashed var(--muted)",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "fontSize": "10px",
                            "color": "var(--muted)",
                        },
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                id="header-hotel-name",
                                children="Grand Riviera Resort",
                                style={"fontWeight": "700", "fontSize": "16px"},
                            ),
                            dcc.Dropdown(
                                id="hotel-selector",
                                options=[{"label": h["label"], "value": h["id"]} for h in HOTELS],
                                value=HOTELS[0]["id"],
                                clearable=False,
                                style={"minWidth": "220px", "marginTop": "6px"},
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                "powered by Grap 4",
                style={
                    "color": "var(--muted)",
                    "fontSize": "12px",
                    "letterSpacing": "0.06em",
                },
            ),
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "12px"},
                children=[
                    html.Span("👤", style={"fontSize": "18px"}),
                    html.Span("Username", style={"fontWeight": "600", "fontSize": "14px"}),
                    html.Span("⚙", style={"cursor": "pointer", "opacity": 0.85}),
                    html.Span("⎋", style={"cursor": "pointer", "opacity": 0.85}),
                ],
            ),
        ],
    )


def hotel_label(hotel_id: str) -> str:
    for h in HOTELS:
        if h["id"] == hotel_id:
            return h["label"]
    return HOTELS[0]["label"]
