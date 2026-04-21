"""Dash entry: layout shell and callback registration for hotel food-cost dashboard."""

import dash
from dash import Input, Output, html

from alerts_widget import create_alerts_widget
from dishes_widget import create_dishes_widget, register_dishes_callbacks
from employee_widget import create_employee_widget
from header import create_header, hotel_label
from inventory_widget import create_inventory_widget, register_inventory_callbacks
from revenue_widget import create_revenue_widget, register_revenue_callbacks
from waste_widget import create_waste_widget

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Food cost — hotel dashboard"

app.layout = html.Div(
    style={"maxWidth": "1440px", "margin": "0 auto", "padding": "20px 24px 32px"},
    children=[
        create_header(),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(3, minmax(0, 1fr))",
                "gap": "16px",
                "marginBottom": "16px",
            },
            children=[
                create_alerts_widget(),
                create_revenue_widget(),
                create_inventory_widget(),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "minmax(0, 0.95fr) minmax(0, 1.05fr)",
                "gap": "16px",
                "marginBottom": "16px",
            },
            children=[
                create_waste_widget(),
                create_employee_widget(),
            ],
        ),
        create_dishes_widget(),
    ],
)


@app.callback(Output("header-hotel-name", "children"), Input("hotel-selector", "value"))
def sync_hotel_title(hotel_id):
    return hotel_label(hotel_id)


register_revenue_callbacks(app)
register_inventory_callbacks(app)
register_dishes_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
