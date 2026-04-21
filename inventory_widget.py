"""Inventory categories, lots, segmented stock bars, search filter."""

from dash import Input, Output, dcc, html

INVENTORY = [
    {
        "category": "Food",
        "kg": 1240,
        "segments": [45, 35, 20],
        "lots": [
            {"name": "LOT #1", "kg": 520, "segments": [50, 30, 20], "expiry": "ok"},
            {"name": "LOT #2", "kg": 410, "segments": [40, 40, 20], "expiry": "warn"},
            {"name": "LOT #3", "kg": 310, "segments": [30, 25, 45], "expiry": "critical"},
        ],
    },
    {
        "category": "Beverages",
        "kg": 210,
        "segments": [60, 30, 10],
        "lots": [
            {"name": "LOT #1", "kg": 120, "segments": [70, 20, 10], "expiry": "ok"},
            {"name": "LOT #2", "kg": 90, "segments": [45, 35, 20], "expiry": "warn"},
        ],
    },
    {
        "category": "Pastry / frozen",
        "kg": 380,
        "segments": [25, 35, 40],
        "lots": [
            {"name": "LOT #1", "kg": 200, "segments": [20, 30, 50], "expiry": "critical"},
            {"name": "LOT #2", "kg": 180, "segments": [35, 40, 25], "expiry": "warn"},
        ],
    },
]

SEG_COLORS = ["#3fb950", "#d29922", "#f85149"]


def _segment_bar(widths, height="12px"):
    return html.Div(
        style={
            "display": "flex",
            "height": height,
            "borderRadius": "6px",
            "overflow": "hidden",
            "border": "1px solid var(--border)",
        },
        children=[
            html.Div(
                style={"width": f"{w}%", "background": SEG_COLORS[i], "height": "100%"},
            )
            for i, w in enumerate(widths)
        ],
    )


def _lot_row(lot):
    exp = lot["expiry"]
    border = (
        "1px solid var(--red)"
        if exp == "critical"
        else "1px solid var(--yellow)"
        if exp == "warn"
        else "1px solid var(--border)"
    )
    return html.Div(
        style={
            "padding": "8px 0 8px 12px",
            "borderLeft": border,
            "marginLeft": "4px",
        },
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "6px",
                    "gap": "8px",
                },
                children=[
                    html.Span(lot["name"], style={"fontSize": "12px", "fontWeight": "600"}),
                    html.Div(
                        style={"display": "flex", "gap": "8px", "alignItems": "center"},
                        children=[
                            html.Span(f"{lot['kg']} kg", style={"fontSize": "11px", "color": "var(--muted)"}),
                            html.Span("🗑", style={"cursor": "pointer", "opacity": 0.75}),
                            html.Span("📅", style={"cursor": "pointer", "opacity": 0.75}),
                        ],
                    ),
                ],
            ),
            _segment_bar(lot["segments"], height="8px"),
        ],
    )


def _filter_inventory(query: str):
    q = (query or "").strip().lower()
    if not q:
        return INVENTORY
    return [row for row in INVENTORY if q in row["category"].lower() or any(q in lot["name"].lower() for lot in row["lots"])]


def _inventory_body(rows):
    blocks = []
    for row in rows:
        blocks.append(
            html.Div(
                style={"marginBottom": "16px"},
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                            "marginBottom": "8px",
                        },
                        children=[
                            html.Span(row["category"], style={"fontWeight": "700", "fontSize": "14px"}),
                            html.Span(f"{row['kg']} kg", style={"fontSize": "12px", "color": "var(--muted)"}),
                        ],
                    ),
                    _segment_bar(row["segments"]),
                    html.Div(
                        style={"marginTop": "10px", "display": "flex", "flexDirection": "column", "gap": "4px"},
                        children=[_lot_row(lot) for lot in row["lots"]],
                    ),
                ],
            )
        )
    if not blocks:
        return html.Div("No categories match your search.", style={"color": "var(--muted)", "fontSize": "13px"})
    return html.Div(blocks)


def create_inventory_widget():
    return html.Div(
        className="panel",
        style={"minHeight": "280px"},
        children=[
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                children=[
                    html.H3("Inventory", className="panel-title", style={"margin": 0}),
                ],
            ),
            html.Div(
                style={"display": "flex", "gap": "8px", "marginBottom": "12px"},
                children=[
                    dcc.Input(
                        id="inventory-search",
                        type="text",
                        placeholder="Search category or lot…",
                        debounce=True,
                        style={
                            "flex": 1,
                            "padding": "8px 12px",
                            "borderRadius": "8px",
                            "border": "1px solid var(--border)",
                            "background": "var(--surface-2)",
                            "color": "var(--text)",
                        },
                    ),
                    html.Span("🔍", style={"alignSelf": "center", "opacity": 0.6}),
                    html.Span("⚙", style={"alignSelf": "center", "cursor": "pointer", "opacity": 0.75}),
                ],
            ),
            html.Div(
                style={"fontSize": "10px", "color": "var(--muted)", "marginBottom": "8px"},
                children="Bar colors: green adequate · yellow watch · red critical (incl. expiration risk)",
            ),
            html.Div(id="inventory-list"),
        ],
    )


def register_inventory_callbacks(app):
    @app.callback(Output("inventory-list", "children"), Input("inventory-search", "value"))
    def filter_list(q):
        return _inventory_body(_filter_inventory(q))
