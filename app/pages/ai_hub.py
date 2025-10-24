import reflex as rx
from app.components.layout import main_layout


def ai_hub_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.h2("AI Analysis Hub", class_name="text-xl font-semibold mb-4"),
            rx.el.p("AI analysis hub page content will go here."),
            class_name="bg-white p-6 rounded-xl border",
        ),
        title="AI Analysis Hub",
    )