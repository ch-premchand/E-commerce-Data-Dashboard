import reflex as rx
from app.states.category_state import CategoryState, CategoryHealth


def comparison_table() -> rx.Component:
    headers = [
        "Category",
        "Health Score",
        "Products",
        "Avg Price",
        "Avg Discount",
        "Avg Colors",
    ]
    return rx.el.div(
        rx.el.h2(
            "Category Comparison Matrix",
            class_name="text-xl font-bold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            headers,
                            lambda header: rx.el.th(
                                header,
                                class_name="p-3 text-left text-sm font-semibold text-gray-600",
                            ),
                        ),
                        class_name="border-b border-gray-200 bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        CategoryState.category_health_scores,
                        lambda category: rx.el.tr(
                            rx.el.td(
                                category["name"],
                                class_name="p-3 text-sm text-gray-700 font-medium",
                            ),
                            rx.el.td(
                                category["health_score"],
                                class_name="p-3 text-sm text-gray-800 font-bold",
                            ),
                            rx.el.td(
                                category["product_count"],
                                class_name="p-3 text-sm text-gray-700",
                            ),
                            rx.el.td(
                                f"${category['avg_price']}",
                                class_name="p-3 text-sm text-gray-700",
                            ),
                            rx.el.td(
                                f"{category['avg_discount']}%",
                                class_name="p-3 text-sm text-gray-700",
                            ),
                            rx.el.td(
                                category["avg_colors"],
                                class_name="p-3 text-sm text-gray-700",
                            ),
                            class_name="border-b border-gray-100 hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-lg border border-gray-200",
        ),
        class_name="p-6 bg-white rounded-xl border",
    )