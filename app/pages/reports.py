import reflex as rx
from app.components.layout import main_layout


def reports_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.h2("Reports & Insights", class_name="text-xl font-semibold mb-4"),
            rx.el.p("Reports and insights page content will go here."),
            class_name="bg-white p-6 rounded-xl border",
        ),
        title="Reports & Insights",
    )