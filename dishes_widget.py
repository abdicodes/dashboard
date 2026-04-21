"""Dish cards: margins, costs, expandable ingredient table."""

from dash import Input, Output, MATCH, ctx, html

DISHES = [
    {
        "name": "Catch of the day",
        "status": "ok",
        "left": 18,
        "price": 26.0,
        "margin": 11.2,
        "food_cost": 8.4,
        "labor_cost": 6.4,
        "ingredients": [
            ("Fish fillet", "180 g", "6.2 kg"),
            ("Citrus butter", "25 g", "4.1 kg"),
            ("Seasonal veg", "90 g", "12 kg"),
        ],
    },
    {
        "name": "Beef tenderloin",
        "status": "warn",
        "left": 6,
        "price": 38.0,
        "margin": 9.5,
        "food_cost": 14.2,
        "labor_cost": 14.3,
        "ingredients": [
            ("Beef tenderloin", "220 g", "3.8 kg"),
            ("Red wine jus", "45 ml", "8 L"),
            ("Potato gratin", "120 g", "9 kg"),
        ],
    },
    {
        "name": "Vegan tasting",
        "status": "critical",
        "left": 22,
        "price": 34.0,
        "margin": 6.1,
        "food_cost": 12.8,
        "labor_cost": 15.1,
        "ingredients": [
            ("Heirloom carrots", "140 g", "5 kg"),
            ("Cashew cream", "60 g", "2.4 kg"),
            ("Herb oil", "15 ml", "3 L"),
        ],
    },
]

STATUS_COLOR = {"ok": "var(--green)", "warn": "var(--yellow)", "critical": "var(--red)"}


def _dish_card(dish, idx):
    ing_rows = [
        html.Tr(
            [
                html.Td(ing, style={"padding": "6px 8px", "fontSize": "12px"}),
                html.Td(amt, style={"padding": "6px 8px", "fontSize": "12px", "color": "var(--muted)"}),
                html.Td(left, style={"padding": "6px 8px", "fontSize": "12px", "color": "var(--muted)"}),
            ]
        )
        for ing, amt, left in dish["ingredients"]
    ]

    return html.Div(
        className="panel",
        style={"marginBottom": "14px", "padding": "16px 18px"},
        children=[
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "gap": "12px"},
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "10px"},
                        children=[
                            html.Span(
                                style={
                                    "width": "12px",
                                    "height": "12px",
                                    "borderRadius": "50%",
                                    "background": STATUS_COLOR[dish["status"]],
                                    "flexShrink": 0,
                                }
                            ),
                            html.H2(
                                dish["name"],
                                style={"margin": 0, "fontSize": "18px", "fontWeight": "700"},
                            ),
                        ],
                    ),
                    html.Span("✎", style={"cursor": "pointer", "opacity": 0.8}),
                ],
            ),
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(140px, 1fr))",
                    "gap": "12px",
                    "marginTop": "14px",
                },
                children=[
                    html.Div(
                        [
                            html.Div("LEFT", style={"fontSize": "10px", "color": "var(--muted)", "letterSpacing": "0.08em"}),
                            html.Div(f"{dish['left']} portions", style={"fontWeight": "700", "marginTop": "4px"}),
                        ]
                    ),
                    html.Div(
                        [
                            html.Div("Selling at", style={"fontSize": "10px", "color": "var(--muted)", "letterSpacing": "0.08em"}),
                            html.Div(
                                [
                                    html.Span(f"{dish['price']:.0f} €", style={"fontWeight": "700"}),
                                    html.Span(
                                        f" → margin {dish['margin']:.1f} €",
                                        style={"marginLeft": "6px", "fontSize": "12px", "color": "var(--muted)"},
                                    ),
                                ],
                                style={"marginTop": "4px"},
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Div("Food cost", style={"fontSize": "10px", "color": "var(--muted)", "letterSpacing": "0.08em"}),
                            html.Div(f"{dish['food_cost']:.1f} €", style={"fontWeight": "700", "marginTop": "4px"}),
                        ]
                    ),
                    html.Div(
                        [
                            html.Div("Labor cost", style={"fontSize": "10px", "color": "var(--muted)", "letterSpacing": "0.08em"}),
                            html.Div(f"{dish['labor_cost']:.1f} €", style={"fontWeight": "700", "marginTop": "4px"}),
                        ]
                    ),
                ],
            ),
            html.Button(
                "Ingredients ▾",
                id={"type": "ing-toggle", "index": idx},
                n_clicks=0,
                style={
                    "marginTop": "14px",
                    "width": "100%",
                    "textAlign": "left",
                    "padding": "10px 12px",
                    "borderRadius": "8px",
                    "border": "1px solid var(--border)",
                    "background": "var(--surface-2)",
                    "color": "var(--text)",
                    "cursor": "pointer",
                    "fontWeight": "600",
                    "fontSize": "13px",
                },
            ),
            html.Div(
                id={"type": "ing-panel", "index": idx},
                style={"display": "none", "marginTop": "8px"},
                children=[
                    html.Table(
                        style={
                            "width": "100%",
                            "borderCollapse": "collapse",
                            "border": "1px solid var(--border)",
                            "borderRadius": "8px",
                            "overflow": "hidden",
                        },
                        children=[
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Ingr.", style={"textAlign": "left", "padding": "8px", "background": "var(--surface-2)", "fontSize": "11px"}),
                                        html.Th(
                                            "amount / dish",
                                            style={"textAlign": "left", "padding": "8px", "background": "var(--surface-2)", "fontSize": "11px"},
                                        ),
                                        html.Th(
                                            "left in inventory",
                                            style={"textAlign": "left", "padding": "8px", "background": "var(--surface-2)", "fontSize": "11px"},
                                        ),
                                    ]
                                )
                            ),
                            html.Tbody(ing_rows),
                        ],
                    )
                ],
            ),
        ],
    )


def create_dishes_widget():
    return html.Div(
        children=[
            html.H3("Dishes", className="panel-title", style={"margin": "0 0 12px 4px"}),
            html.Div([_dish_card(d, i) for i, d in enumerate(DISHES)]),
        ]
    )


def register_dishes_callbacks(app):
    @app.callback(
        Output({"type": "ing-panel", "index": MATCH}, "style"),
        Input({"type": "ing-toggle", "index": MATCH}, "n_clicks"),
    )
    def toggle_ingredients(n):
        n = n or 0
        return {"display": "block"} if n % 2 == 1 else {"display": "none"}
