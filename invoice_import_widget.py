"""Invoice upload widget: import local AP-grid-like files and generate analysis."""

import base64
import csv
import io

import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html


FIELD_ALIASES = {
    "supplier": ["supplier", "fornitore", "denominazione", "cedente/prestatore"],
    "category": ["category", "categoria", "reparto"],
    "channel": ["channel", "canale"],
    "qty": ["qty_kg", "quantità", "quantita", "qta", "quantita_kg"],
    "unit_price": ["unit_price_eur", "prezzo unitario", "prezzo_unitario", "prezzo"],
    "total_price": ["prezzo totale", "prezzo_totale", "totale_riga", "line_total_eur"],
    "vat": ["%iva", "iva", "aliquota iva"],
    "description": ["descrizione", "item", "prodotto"],
    "waste_kg": ["waste_kg", "scarto_kg"],
}


def _empty_figure():
    fig = go.Figure()
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text="Upload AP invoice file to generate analysis",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(color="#8b949e", size=13),
            )
        ],
    )
    return fig


def _bar_figure(categories):
    labels = [k for k, _ in categories]
    values = [v for _, v in categories]
    fig = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker=dict(color="#58a6ff"),
                text=[f"€ {v:,.0f}" for v in values],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=10, r=20, t=10, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6edf3"),
        xaxis=dict(gridcolor="#2a3140", zeroline=False),
        yaxis=dict(autorange="reversed"),
        height=220,
    )
    return fig


def create_invoice_import_widget():
    return html.Div(
        className="panel",
        style={"marginBottom": "16px"},
        children=[
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "gap": "16px", "flexWrap": "wrap"},
                children=[
                    html.Div(
                        children=[
                            html.H3("Invoice import", className="panel-title", style={"marginBottom": "8px"}),
                            html.Div(
                                "Import AP-style invoice CSV (supports Grid EInvoice-like columns) to auto-generate analysis.",
                                style={"fontSize": "13px", "color": "var(--muted)"},
                            ),
                        ]
                    ),
                    html.Div(
                        style={"display": "flex", "gap": "8px"},
                        children=[
                            html.Button(
                                "Download sample A",
                                id="download-sample-a-btn",
                                n_clicks=0,
                                style={
                                    "padding": "8px 12px",
                                    "borderRadius": "8px",
                                    "border": "1px solid var(--border)",
                                    "background": "var(--surface-2)",
                                    "color": "var(--text)",
                                    "cursor": "pointer",
                                },
                            ),
                            html.Button(
                                "Download sample B",
                                id="download-sample-b-btn",
                                n_clicks=0,
                                style={
                                    "padding": "8px 12px",
                                    "borderRadius": "8px",
                                    "border": "1px solid var(--border)",
                                    "background": "var(--surface-2)",
                                    "color": "var(--text)",
                                    "cursor": "pointer",
                                },
                            ),
                            dcc.Download(id="download-sample-file"),
                        ],
                    ),
                ],
            ),
            html.Div(
                style={"marginTop": "12px", "display": "flex", "gap": "10px", "alignItems": "center", "flexWrap": "wrap"},
                children=[
                    dcc.Upload(
                        id="invoice-upload",
                        children=html.Button(
                            "Import invoice file",
                            style={
                                "padding": "9px 14px",
                                "borderRadius": "8px",
                                "border": "1px solid var(--accent)",
                                "background": "#0d2238",
                                "color": "var(--text)",
                                "cursor": "pointer",
                                "fontWeight": "600",
                            },
                        ),
                        multiple=False,
                    ),
                    html.Span("Expected format: CSV (comma or semicolon)", style={"fontSize": "12px", "color": "var(--muted)"}),
                    html.Span(id="invoice-upload-status", style={"fontSize": "12px"}),
                ],
            ),
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(4, minmax(0, 1fr))",
                    "gap": "10px",
                    "marginTop": "14px",
                },
                children=[
                    html.Div(className="panel", style={"padding": "10px 12px", "background": "var(--surface-2)"}, children=[html.Div("Invoice spend", style={"fontSize": "11px", "color": "var(--muted)"}), html.Div(id="invoice-kpi-total", style={"fontSize": "22px", "fontWeight": "700", "marginTop": "3px"})]),
                    html.Div(className="panel", style={"padding": "10px 12px", "background": "var(--surface-2)"}, children=[html.Div("Lines imported", style={"fontSize": "11px", "color": "var(--muted)"}), html.Div(id="invoice-kpi-lines", style={"fontSize": "22px", "fontWeight": "700", "marginTop": "3px"})]),
                    html.Div(className="panel", style={"padding": "10px 12px", "background": "var(--surface-2)"}, children=[html.Div("Waste cost", style={"fontSize": "11px", "color": "var(--muted)"}), html.Div(id="invoice-kpi-waste", style={"fontSize": "22px", "fontWeight": "700", "marginTop": "3px"})]),
                    html.Div(className="panel", style={"padding": "10px 12px", "background": "var(--surface-2)"}, children=[html.Div("Internal coverage", style={"fontSize": "11px", "color": "var(--muted)"}), html.Div(id="invoice-kpi-internal", style={"fontSize": "22px", "fontWeight": "700", "marginTop": "3px"})]),
                ],
            ),
            dcc.Graph(
                id="invoice-category-chart",
                figure=_empty_figure(),
                config={"displayModeBar": False},
                style={"marginTop": "10px"},
            ),
        ],
    )


def _parse_num(value):
    if value is None:
        return 0.0
    text = str(value).strip().replace("€", "").replace(" ", "")
    if not text:
        return 0.0
    # Support Italian decimal format (e.g. 7,132) and common thousand separators.
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0


def _normalize_header(name):
    return (name or "").strip().lower().replace("_", " ")


def _pick(row, aliases, default=""):
    for key in row.keys():
        norm = _normalize_header(key)
        for alias in aliases:
            if _normalize_header(alias) == norm:
                return row.get(key, default)
    return default


def _infer_category(description):
    d = (description or "").lower()
    if any(k in d for k in ["vino", "water", "beer", "birra", "champagne", "acqua"]):
        return "Beverages"
    if any(k in d for k in ["gelato", "croissant", "pastry", "panna", "yogurt"]):
        return "Pastry / frozen"
    return "Food"


def _parse_invoice_contents(contents):
    if not contents:
        return []

    _, encoded = contents.split(",", 1)
    raw_bytes = base64.b64decode(encoded)
    try:
        raw = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw = raw_bytes.decode("latin-1")

    sample = raw[:3000]
    try:
        delimiter = csv.Sniffer().sniff(sample, delimiters=";,").delimiter
    except csv.Error:
        delimiter = ","

    reader = csv.DictReader(io.StringIO(raw), delimiter=delimiter)
    rows = []
    for row in reader:
        qty = _parse_num(_pick(row, FIELD_ALIASES["qty"], 0))
        unit = _parse_num(_pick(row, FIELD_ALIASES["unit_price"], 0))
        row_total = _parse_num(_pick(row, FIELD_ALIASES["total_price"], 0))
        waste = _parse_num(_pick(row, FIELD_ALIASES["waste_kg"], 0))
        spend = row_total if row_total > 0 else qty * unit
        waste_cost = waste * unit

        description = str(_pick(row, FIELD_ALIASES["description"], "") or "").strip()
        category = str(_pick(row, FIELD_ALIASES["category"], "") or "").strip() or _infer_category(description)
        supplier = str(_pick(row, FIELD_ALIASES["supplier"], "unknown") or "unknown").strip()
        channel = str(_pick(row, FIELD_ALIASES["channel"], "") or "").strip().lower()
        if channel not in {"internal", "external"}:
            # Grid-like AP exports often do not include channel; use VAT as a practical proxy.
            vat = _parse_num(_pick(row, FIELD_ALIASES["vat"], 0))
            channel = "internal" if vat <= 4 else "external"

        rows.append(
            {
                "category": category,
                "supplier": supplier,
                "channel": channel,
                "spend": spend,
                "waste_cost": waste_cost,
            }
        )
    return rows


def register_invoice_import_callbacks(app):
    @app.callback(
        Output("download-sample-file", "data"),
        Input("download-sample-a-btn", "n_clicks"),
        Input("download-sample-b-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_samples(_a, _b):
        from dash import ctx

        trig = ctx.triggered_id
        if trig == "download-sample-a-btn":
            return dcc.send_file("sample_invoices/invoice_example_a.csv")
        return dcc.send_file("sample_invoices/invoice_example_b.csv")

    @app.callback(
        Output("invoice-upload-status", "children"),
        Output("invoice-upload-status", "style"),
        Output("invoice-kpi-total", "children"),
        Output("invoice-kpi-lines", "children"),
        Output("invoice-kpi-waste", "children"),
        Output("invoice-kpi-internal", "children"),
        Output("invoice-category-chart", "figure"),
        Input("invoice-upload", "contents"),
        State("invoice-upload", "filename"),
    )
    def analyze_invoice(contents, filename):
        if not contents:
            return (
                "No file imported yet.",
                {"color": "var(--muted)"},
                "€ 0",
                "0",
                "€ 0",
                "0%",
                _empty_figure(),
            )

        try:
            rows = _parse_invoice_contents(contents)
            if not rows:
                return (
                    "File has no rows.",
                    {"color": "var(--yellow)"},
                    "€ 0",
                    "0",
                    "€ 0",
                    "0%",
                    _empty_figure(),
                )

            total_spend = sum(r["spend"] for r in rows)
            total_waste = sum(r["waste_cost"] for r in rows)
            internal_spend = sum(r["spend"] for r in rows if r["channel"] == "internal")
            internal_pct = 0 if total_spend == 0 else (internal_spend / total_spend) * 100

            by_category = {}
            for r in rows:
                by_category[r["category"]] = by_category.get(r["category"], 0) + r["spend"]
            top_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:6]

            return (
                f"Imported {filename}",
                {"color": "var(--green)"},
                f"€ {total_spend:,.0f}",
                f"{len(rows)}",
                f"€ {total_waste:,.0f}",
                f"{internal_pct:.1f}%",
                _bar_figure(top_categories),
            )
        except Exception as exc:
            return (
                f"Import failed: {exc}",
                {"color": "var(--red)"},
                "€ 0",
                "0",
                "€ 0",
                "0%",
                _empty_figure(),
            )
