import reflex as rx
from app.components.layout import main_layout
from app.components.product_grid import (
    product_grid,
    product_list_view,
    product_view_controls,
    pagination_controls,
)
from app.states.product_state import ProductState


def filter_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.h3("Filters", class_name="text-lg font-semibold mb-4"),
        rx.el.div(
            rx.el.div(
                rx.el.h4("Category", class_name="font-semibold mb-2 text-sm"),
                rx.el.div(
                    rx.foreach(
                        ProductState.all_categories,
                        lambda category: rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                on_change=ProductState.toggle_category_filter(category),
                                checked=ProductState.selected_categories.contains(
                                    category
                                ),
                                class_name="h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500",
                            ),
                            rx.el.span(
                                category, class_name="ml-2 text-sm text-gray-700"
                            ),
                            rx.el.span(f" ({ProductState.category_counts[category]})"),
                            class_name="flex items-center mb-1",
                        ),
                    ),
                    class_name="space-y-1 h-64 overflow-y-auto pr-2",
                ),
                class_name="py-4 border-b",
            ),
            rx.el.div(
                rx.el.h4("Price Range", class_name="font-semibold mb-2 text-sm"),
                rx.el.p(
                    f"${ProductState.price_range[0].to_string()} - ${ProductState.price_range[1].to_string()}"
                ),
                class_name="py-4 border-b",
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        on_change=ProductState.set_show_discounts_only,
                        checked=ProductState.show_discounts_only,
                        class_name="h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500",
                    ),
                    rx.el.span(
                        "Show only discounted items",
                        class_name="ml-2 text-sm text-gray-700",
                    ),
                    class_name="flex items-center",
                ),
                class_name="py-4",
            ),
            rx.el.button(
                "Clear All Filters",
                on_click=ProductState.clear_all_filters,
                disabled=ProductState.active_filter_count == 0,
                class_name="w-full mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50",
            ),
            class_name="space-y-4",
        ),
        class_name="w-72 p-4 bg-white border-r h-full overflow-y-auto",
    )


def products_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            filter_sidebar(),
            rx.el.div(
                product_view_controls(),
                rx.match(
                    ProductState.view_mode,
                    ("grid", product_grid()),
                    ("list", product_list_view()),
                    product_grid(),
                ),
                pagination_controls(),
                class_name="flex-1 p-6 space-y-4",
            ),
            class_name="flex flex-1",
        ),
        title="Products Explorer",
    )