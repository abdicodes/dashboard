"""Revenue tabs, comparison trend, internal vs external split, sparkline, detail modal."""

import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html

PERIODS = ["DAY", "MONTH", "SEASONAL", "YEAR"]

REVENUE_DATA = {
    "DAY": {"value": 12840, "delta": 4.2, "internal": 62, "external": 38},
    "MONTH": {"value": 382900, "delta": -1.1, "internal": 58, "external": 42},
    "SEASONAL": {"value": 1120000, "delta": 6.8, "internal": 55, "external": 45},
    "YEAR": {"value": 4280000, "delta": 3.4, "internal": 60, "external": 40},
}


def _trend_arrow(delta: float) -> html.Span:
    if delta > 0.05:
        return html.Span(" ▲", className="trend-up")
    if delta < -0.05:
        return html.Span(" ▼", className="trend-down")
    return html.Span(" ▬", className="trend-flat")


def _sparkline():
    y = [92, 88, 90, 95, 93, 97, 101, 99, 103, 105, 102, 108]
    fig = go.Figure(
        data=go.Scatter(
            y=y,
            mode="lines",
            line=dict(color="#58a6ff", width=2),
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.12)",
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=48,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


def create_revenue_widget():
    tab_style = {
        "padding": "10px 16px",
        "fontWeight": "600",
        "fontSize": "11px",
        "letterSpacing": "0.06em",
        "border": "1px solid var(--border)",
        "background": "var(--surface-2)",
        "color": "var(--muted)",
        "borderRadius": "8px",
        "marginRight": "8px",
    }
    selected = {
        **tab_style,
        "background": "#21262d",
        "color": "var(--text)",
        "borderColor": "var(--accent)",
    }

    tabs = dcc.Tabs(
        id="revenue-tabs",
        value="DAY",
        children=[dcc.Tab(label=p, value=p, style=tab_style, selected_style=selected) for p in PERIODS],
        style={"marginBottom": "14px"},
        parent_style={"borderBottom": "none"},
    )

    detail = html.Div(
        id="revenue-detail-backdrop",
        style={
            "display": "none",
            "position": "fixed",
            "inset": 0,
            "background": "rgba(0,0,0,0.55)",
            "zIndex": 1000,
            "alignItems": "center",
            "justifyContent": "center",
            "padding": "24px",
        },
        children=[
            html.Div(
                style={
                    "background": "var(--surface)",
                    "border": "1px solid var(--border)",
                    "borderRadius": "12px",
                    "maxWidth": "420px",
                    "width": "100%",
                    "padding": "20px",
                },
                children=[
                    html.Div(
                        "Internal vs external revenue",
                        style={"fontWeight": "700", "marginBottom": "10px"},
                    ),
                    html.P(
                        "Internal covers in-house guests (rooms, packages, staff meals). "
                        "External is walk-ins, events, and third-party channels. "
                        "Split is accrual-based for the selected period.",
                        style={"fontSize": "13px", "color": "var(--muted)", "lineHeight": 1.5},
                    ),
                    html.Button(
                        "Close",
                        id="revenue-detail-close",
                        n_clicks=0,
                        style={
                            "marginTop": "16px",
                            "padding": "8px 16px",
                            "borderRadius": "8px",
                            "border": "1px solid var(--border)",
                            "background": "var(--surface-2)",
                            "color": "var(--text)",
                            "cursor": "pointer",
                        },
                    ),
                ],
            )
        ],
    )

    return html.Div(
        [
            html.Div(
                className="panel",
                style={"minHeight": "280px"},
                children=[
                    html.H3("Revenue", className="panel-title"),
                    tabs,
                    html.Div(id="revenue-primary-row", style={"display": "flex", "alignItems": "baseline", "gap": "8px"}),
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            html.Div(
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "marginBottom": "6px",
                                    "fontSize": "12px",
                                    "color": "var(--muted)",
                                },
                                children=[
                                    html.Span("Internal / Ext."),
                                    html.Button(
                                        "Detailed info",
                                        id="revenue-detail-open",
                                        n_clicks=0,
                                        style={
                                            "background": "none",
                                            "border": "none",
                                            "color": "var(--accent)",
                                            "cursor": "pointer",
                                            "fontSize": "12px",
                                            "padding": 0,
                                            "textDecoration": "underline",
                                        },
                                    ),
                                ],
                            ),
                            html.Div(
                                id="revenue-split-bar",
                                style={
                                    "height": "12px",
                                    "borderRadius": "6px",
                                    "overflow": "hidden",
                                    "display": "flex",
                                    "border": "1px solid var(--border)",
                                },
                            ),
                            html.Div(
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "12px",
                                    "marginTop": "10px",
                                },
                                children=[
                                    html.Div(
                                        id="revenue-split-legend",
                                        style={"flex": "1", "fontSize": "11px", "color": "var(--muted)"},
                                    ),
                                    html.Div(
                                        className="sparkline-wrap",
                                        style={"width": "120px", "flexShrink": 0},
                                        children=[
                                            dcc.Graph(
                                                id="revenue-sparkline",
                                                figure=_sparkline(),
                                                config={"displayModeBar": False},
                                                style={"height": "52px"},
                                            )
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            detail,
        ]
    )


def _format_currency(n: float) -> str:
    if n >= 1_000_000:
        return f"€ {n/1_000_000:.2f}M"
    if n >= 1000:
        return f"€ {n/1000:.1f}k"
    return f"€ {n:,.0f}"


def register_revenue_callbacks(app):
    @app.callback(
        Output("revenue-primary-row", "children"),
        Output("revenue-split-bar", "children"),
        Output("revenue-split-legend", "children"),
        Input("revenue-tabs", "value"),
    )
    def update_revenue(period):
        period = period or "DAY"
        d = REVENUE_DATA.get(period, REVENUE_DATA["DAY"])
        delta = d["delta"]
        primary = html.Div(
            [
                html.Span(
                    _format_currency(d["value"]),
                    style={"fontSize": "28px", "fontWeight": "700"},
                ),
                html.Span(
                    [
                        html.Span(
                            f" vs last {period.lower()} {delta:+.1f}%",
                            style={"fontSize": "13px", "color": "var(--muted)"},
                        ),
                        _trend_arrow(delta),
                    ]
                ),
            ],
            style={"display": "flex", "flexWrap": "wrap", "alignItems": "baseline", "gap": "8px"},
        )

        inn, ext = d["internal"], d["external"]
        bar_children = [
            html.Div(
                style={
                    "width": f"{inn}%",
                    "background": "linear-gradient(90deg, #238636, #3fb950)",
                    "height": "100%",
                },
                title=f"Internal {inn}%",
            ),
            html.Div(
                style={
                    "width": f"{ext}%",
                    "background": "linear-gradient(90deg, #a371f7, #8957e5)",
                    "height": "100%",
                },
                title=f"External {ext}%",
            ),
        ]
        legend = html.Span(f"Internal {inn}% · External {ext}%")
        return primary, bar_children, legend

    @app.callback(
        Output("revenue-detail-backdrop", "style"),
        Input("revenue-detail-open", "n_clicks"),
        Input("revenue-detail-close", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_detail(_o, _c):
        from dash import ctx

        trig = ctx.triggered_id
        base = {
            "position": "fixed",
            "inset": 0,
            "background": "rgba(0,0,0,0.55)",
            "zIndex": 1000,
            "alignItems": "center",
            "justifyContent": "center",
            "padding": "24px",
        }
        if trig == "revenue-detail-open":
            return {**base, "display": "flex"}
        return {**base, "display": "none"}
