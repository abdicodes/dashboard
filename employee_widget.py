"""Employees presence grid with per-day status and staffing warning."""

from datetime import date, timedelta

from dash import html

def _dates_header(n=7):
    start = date.today()
    return [start + timedelta(days=i) for i in range(n)]


# mock: enough / low staffing
def _mock_rows(dates):
    names = [
        ("Elena Rossi", "Head Chef"),
        ("Jonas Meyer", "Sous Chef"),
        ("Aisha Khan", "Line"),
        ("Marco Bianchi", "Line"),
        ("Sofia Anders", "Pastry"),
        ("Liam O'Neil", "Steward"),
    ]
    # status: present, off, sick
    statuses = [
        ["present", "present", "present", "off", "present", "present", "present"],
        ["present", "present", "present", "present", "off", "present", "present"],
        ["present", "sick", "present", "present", "present", "off", "present"],
        ["present", "present", "present", "present", "present", "present", "off"],
        ["off", "present", "present", "present", "present", "present", "present"],
        ["present", "present", "off", "present", "present", "present", "present"],
    ]
    return list(zip(names, statuses))


def _shield(status: str):
    colors = {
        "present": "#3fb950",
        "off": "#8b949e",
        "sick": "#d29922",
    }
    c = colors.get(status, "#8b949e")
    return html.Span(
        "⬡",
        style={
            "color": c,
            "fontSize": "16px",
            "display": "inline-block",
            "lineHeight": 1,
        },
        title=status.capitalize(),
    )


def _coverage_warning(dates, rows):
    """Warn if any day has fewer than 4 'present' across kitchen roles."""
    low_days = []
    for di, _ in enumerate(dates):
        present = sum(1 for _, st in rows if st[di] == "present")
        if present < 4:
            low_days.append(dates[di].strftime("%d %b"))
    if not low_days:
        return None
    return f"Warning: low staffing on {', '.join(low_days)} — review shifts."


def create_employee_widget():
    dates = _dates_header()
    rows = _mock_rows(dates)
    warn = _coverage_warning(dates, rows)

    head_cells = [
        html.Th("Name", style={"textAlign": "left", "padding": "8px", "fontSize": "11px", "color": "var(--muted)"}),
        html.Th("Role", style={"textAlign": "left", "padding": "8px", "fontSize": "11px", "color": "var(--muted)"}),
    ]
    for d in dates:
        label = "Today" if d == date.today() else d.strftime("%d")
        head_cells.append(
            html.Th(
                label,
                style={"textAlign": "center", "padding": "8px 4px", "fontSize": "11px", "color": "var(--muted)", "minWidth": "36px"},
            )
        )

    body_rows = []
    for (name, role), st in rows:
        cells = [
            html.Td(name, style={"padding": "8px", "fontSize": "13px", "fontWeight": "600"}),
            html.Td(role, style={"padding": "8px", "fontSize": "12px", "color": "var(--muted)"}),
        ]
        for s in st:
            cells.append(html.Td(_shield(s), style={"textAlign": "center", "padding": "6px 4px"}))
        body_rows.append(html.Tr(cells))

    banner = None
    if warn:
        banner = html.Div(
            warn,
            style={
                "background": "color-mix(in srgb, var(--yellow) 18%, transparent)",
                "border": "1px solid var(--yellow)",
                "color": "var(--text)",
                "padding": "8px 12px",
                "borderRadius": "8px",
                "fontSize": "12px",
                "marginBottom": "12px",
            },
        )

    return html.Div(
        className="panel",
        children=[
            html.H3("Employees presence", className="panel-title"),
            banner,
            html.Div(
                style={"overflowX": "auto"},
                children=[
                    html.Table(
                        style={"width": "100%", "borderCollapse": "collapse"},
                        children=[html.Thead(html.Tr(head_cells)), html.Tbody(body_rows)],
                    )
                ],
            ),
            html.Div(
                style={"marginTop": "10px", "fontSize": "11px", "color": "var(--muted)"},
                children="⬡ Green on duty · Gray off · Amber sick / exception",
            ),
        ],
    )
