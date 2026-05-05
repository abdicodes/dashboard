"""Stylish landing page for the hotel food-cost dashboard."""

from dash import dcc, html


def create_landing_page():
    return html.Div(
        className="landing-root",
        children=[
            html.Div(
                className="landing-bg",
                children=[
                    html.Div(className="blob blob-1"),
                    html.Div(className="blob blob-2"),
                    html.Div(className="blob blob-3"),
                    html.Div(className="gridlines"),
                ],
            ),
            html.Div(
                className="landing-content",
                children=[
                    html.Div(
                        className="landing-topbar",
                        children=[
                            html.Div(
                                className="landing-logo",
                                children=[
                                    html.Div(className="landing-logo-mark", children="G"),
                                    html.Div(
                                        [
                                            html.Div("Grap 4", className="landing-logo-title"),
                                            html.Div("Food cost analytics", className="landing-logo-subtitle"),
                                        ]
                                    ),
                                ],
                            ),
                            html.Div(className="landing-top-actions", children=[html.Span("Try demo ->", className="landing-top-link")]),
                        ],
                    ),
                    html.Div(
                        className="landing-hero",
                        children=[
                            html.H1(
                                "Track food cost across hotels "
                                "from invoices to action",
                                className="landing-hero-title",
                            ),
                            html.P(
                                "Stop guessing and start managing. Upload your AP invoice export, and this dashboard turns it into daily hotel insights: spend by category, waste cost signals, internal vs external coverage, and operational cues (inventory and staffing).",
                                className="landing-hero-subtitle",
                            ),
                            html.Div(
                                className="landing-hero-cta",
                                children=[
                                    html.Div(
                                        className="landing-primary-cta",
                                        children=[
                                            html.Span("Fast demo: import a sample invoice"),
                                            html.Span(" - scroll down and press Try demo", className="landing-primary-cta-sub"),
                                        ],
                                    )
                                ],
                            ),
                            html.Div(
                                className="landing-hero-chips",
                                children=[
                                    html.Span("Multi-hotel overview", className="chip"),
                                    html.Span("Invoice-ready workflow", className="chip"),
                                    html.Span("Waste & inventory signals", className="chip"),
                                    html.Span("Actionable alerts", className="chip"),
                                ],
                            ),
                            html.Div(
                                className="landing-hero-stats",
                                children=[
                                    html.Div(
                                        className="stat-card",
                                        children=[
                                            html.Div("12%", className="stat-value"),
                                            html.Div("Avg waste reduction", className="stat-label"),
                                        ],
                                    ),
                                    html.Div(
                                        className="stat-card",
                                        children=[
                                            html.Div("3–4h", className="stat-value"),
                                            html.Div("Faster invoice review", className="stat-label"),
                                        ],
                                    ),
                                    html.Div(
                                        className="stat-card",
                                        children=[
                                            html.Div("24/7", className="stat-value"),
                                            html.Div("Operational visibility", className="stat-label"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="landing-section landing-section-what",
                        children=[
                            html.Div(className="landing-section-title", children=["Built for hotel cost control"]),
                            html.P(
                                "Whether you manage one property or a group, food cost is rarely a single number. It is a chain: invoices -> portioning -> inventory lots -> kitchen execution -> waste. This landing demo shows the chain as an integrated flow so your team can react faster and with confidence.",
                                className="landing-section-lead",
                            ),
                            html.Div(
                                className="landing-grid landing-grid-3",
                                children=[
                                    html.Div(
                                        className="feature-card feature-card-strong",
                                        children=[
                                            html.Div("Spend", className="feature-index"),
                                            html.Div("Category breakdown that you can trust", className="feature-title"),
                                            html.Div(
                                                "Get spend totals by category from your invoice export, then visualize the biggest drivers immediately. Less time building spreadsheets, more time resolving issues.",
                                                className="feature-body",
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="feature-card feature-card-strong",
                                        children=[
                                            html.Div("Waste signals", className="feature-index"),
                                            html.Div("See where cost leaks happen", className="feature-title"),
                                            html.Div(
                                                "Turn waste quantities into waste cost signals. Highlight periods that look off so you can investigate portions, shrink, and supplier pricing changes.",
                                                className="feature-body",
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="feature-card feature-card-strong",
                                        children=[
                                            html.Div("Operations", className="feature-index"),
                                            html.Div("Inventory value + staffing cues", className="feature-title"),
                                            html.Div(
                                                "Pair financial signals with operational context: inventory lots with risk cues, and team coverage hints. When both align, decisions become much easier.",
                                                className="feature-body",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="landing-section landing-section-how",
                        children=[
                            html.Div(className="landing-section-title", children=["How the demo works"]),
                            html.Div(
                                className="landing-steps",
                                children=[
                                    html.Div(className="step-card", children=[
                                        html.Div("1", className="step-index"),
                                        html.Div("Import an invoice export", className="step-title"),
                                        html.Div("Use the buttons inside the dashboard to load sample files, or upload your own CSV export.", className="step-body"),
                                    ]),
                                    html.Div(className="step-card", children=[
                                        html.Div("2", className="step-index"),
                                        html.Div("Generate analysis instantly", className="step-title"),
                                        html.Div("Spend totals, waste cost, and top categories appear automatically. No manual chart building.", className="step-body"),
                                    ]),
                                    html.Div(className="step-card", children=[
                                        html.Div("3", className="step-index"),
                                        html.Div("Act on signals", className="step-title"),
                                        html.Div("Compare to past patterns and focus attention where margins are at risk (inventory lots + operational cues).", className="step-body"),
                                    ]),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="landing-section landing-section-results",
                        children=[
                            html.Div(className="landing-section-title", children=["What you will get (in this app)"]),
                            html.Div(
                                className="landing-result-grid",
                                children=[
                                    html.Div(className="result-item", children=[
                                        html.Div("Invoices -> category spend", className="result-title"),
                                        html.Div("Top drivers shown as a clean bar chart.", className="result-body"),
                                    ]),
                                    html.Div(className="result-item", children=[
                                        html.Div("Waste cost estimates", className="result-title"),
                                        html.Div("Waste quantity turns into a cost signal.", className="result-body"),
                                    ]),
                                    html.Div(className="result-item", children=[
                                        html.Div("Internal vs external coverage", className="result-title"),
                                        html.Div("A split view to understand where spend originates.", className="result-body"),
                                    ]),
                                    html.Div(className="result-item", children=[
                                        html.Div("Inventory + lot risk cues", className="result-title"),
                                        html.Div("Category value and per-lot € value, plus expiry emphasis.", className="result-body"),
                                    ]),
                                    html.Div(className="result-item", children=[
                                        html.Div("Employee presence overview", className="result-title"),
                                        html.Div("A simple grid that helps spot staffing gaps.", className="result-body"),
                                    ]),
                                    html.Div(className="result-item", children=[
                                        html.Div("Dish margin context", className="result-title"),
                                        html.Div("Dishes show food/labor cost and margin cues, with ingredients.", className="result-body"),
                                    ]),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="landing-section landing-section-social",
                        children=[
                            html.Div(className="landing-section-title", children=["Teams that move faster"]),
                            html.Div(
                                className="landing-testimonials",
                                children=[
                                    html.Div(className="quote-card", children=[
                                        html.Div("“We stopped chasing spreadsheets. The biggest spend drivers and waste signals are visible in minutes.”", className="quote-text"),
                                        html.Div("Ops Manager, multi-hotel group", className="quote-author"),
                                    ]),
                                    html.Div(className="quote-card", children=[
                                        html.Div("“Importing invoice exports is straightforward, and the dashboard immediately tells us what to investigate.”", className="quote-text"),
                                        html.Div("Finance Controller, hospitality", className="quote-author"),
                                    ]),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="landing-section landing-section-faq",
                        children=[
                            html.Div(className="landing-section-title", children=["FAQ"]),
                            html.Div(className="landing-faq-grid", children=[
                                html.Details([
                                    html.Summary("What file format does the import support?"),
                                    html.Div("This demo accepts CSV exports similar to GridEInvoice-like AP tables. The parser tries to detect common invoice columns and numeric formats (including Italian decimals)."),
                                ], open=False, className="faq-item"),
                                html.Details([
                                    html.Summary("Do I need to map categories manually?"),
                                    html.Div("For the demo, categories are inferred from item descriptions or explicit category columns. In a production setup, mapping can be stored per supplier/item."),
                                ], open=False, className="faq-item"),
                                html.Details([
                                    html.Summary("Can I switch hotels?"),
                                    html.Div("Yes. The dashboard includes a hotel selector in the header. In this demo, it changes the displayed hotel name; the same hook can drive hotel-specific analysis later."),
                                ], open=False, className="faq-item"),
                                html.Details([
                                    html.Summary("Is this data secure?"),
                                    html.Div("The demo runs locally in your browser process. When you connect real systems, you can enforce access control and audit logs before storing any invoice details."),
                                ], open=False, className="faq-item"),
                            ]),
                        ],
                    ),
                    html.Div(className="landing-bottom-spacer", children=[html.Div(className="landing-footer-note")]),
                ],
            ),
        ],
    )

