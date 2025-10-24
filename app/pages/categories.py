import reflex as rx
from app.components.layout import main_layout
from app.states.category_state import CategoryState
from app.components.category_cards import category_overview_cards
from app.components.category_comparison import comparison_table
from app.components.category_insights import (
    ai_category_insights_panel,
    category_drill_down,
)


def categories_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.div(
                category_overview_cards(),
                rx.cond(
                    CategoryState.selected_category, category_drill_down(), rx.el.div()
                ),
                comparison_table(),
                class_name="space-y-6 flex-1",
            ),
            rx.cond(
                CategoryState.selected_category,
                ai_category_insights_panel(),
                rx.el.div(
                    rx.el.p(
                        "Select a category to view AI insights.",
                        class_name="text-center text-gray-500",
                    ),
                    class_name="p-6 bg-white rounded-xl border-2 border-dashed flex items-center justify-center sticky top-6 h-48",
                ),
            ),
            class_name="grid lg:grid-cols-3 gap-6 items-start",
        ),
        title="Category Analytics",
    )