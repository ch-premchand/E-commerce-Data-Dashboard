import reflex as rx
from app.states.category_state import CategoryState


def insight_item(title: str, content: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.h4(title, class_name="font-semibold text-gray-700 mb-1"),
        rx.el.div(
            rx.markdown(
                content,
                component_map={
                    "p": lambda text: rx.el.p(text, class_name="text-sm text-gray-600")
                },
            ),
            class_name="prose prose-sm max-w-none text-gray-600",
        ),
    )


def insights_loading_skeleton() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            [1, 2, 3, 4],
            lambda i: rx.el.div(
                rx.el.div(class_name="h-4 w-1/3 bg-gray-200 rounded-md"),
                rx.el.div(class_name="h-3 w-full bg-gray-200 rounded-md mt-2"),
                rx.el.div(class_name="h-3 w-5/6 bg-gray-200 rounded-md mt-1"),
                class_name="mb-4",
            ),
        ),
        class_name="animate-pulse",
    )


def ai_category_insights_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "AI Category Strategy", class_name="text-lg font-semibold text-gray-800"
            ),
            rx.el.p(
                CategoryState.selected_category,
                class_name="text-sm text-emerald-600 font-medium",
            ),
            class_name="flex items-baseline justify-between mb-4",
        ),
        rx.cond(
            CategoryState.is_loading_insights,
            insights_loading_skeleton(),
            rx.cond(
                CategoryState.ai_insights.contains("pricing_strategy"),
                rx.el.div(
                    insight_item(
                        "Pricing Strategy",
                        CategoryState.ai_insights["pricing_strategy"],
                    ),
                    insight_item(
                        "Market Positioning",
                        CategoryState.ai_insights["market_positioning"],
                    ),
                    insight_item(
                        "Inventory Optimization",
                        CategoryState.ai_insights["inventory_optimization"],
                    ),
                    insight_item(
                        "Growth Opportunities",
                        CategoryState.ai_insights["growth_opportunities"],
                    ),
                    rx.el.button(
                        "Regenerate",
                        on_click=CategoryState.generate_category_insights,
                        class_name="w-full mt-4 text-sm font-medium text-emerald-600 hover:text-emerald-800",
                    ),
                    class_name="space-y-4",
                ),
                rx.cond(
                    CategoryState.ai_insights.contains("error"),
                    rx.el.div(
                        rx.el.p(
                            "Error generating insights:",
                            class_name="font-semibold text-red-600",
                        ),
                        rx.el.p(
                            CategoryState.ai_insights["error"],
                            class_name="text-sm text-red-500",
                        ),
                    ),
                    rx.el.button(
                        "Generate Strategy",
                        on_click=CategoryState.generate_category_insights,
                        class_name="w-full px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700",
                    ),
                ),
            ),
        ),
        class_name="p-6 bg-white rounded-xl border-2 border-emerald-100 shadow-sm sticky top-6 h-fit",
    )


def category_drill_down() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            f"Top Products in {CategoryState.selected_category}",
            class_name="text-xl font-bold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Product",
                            class_name="text-left text-sm font-semibold text-gray-600 p-3",
                        ),
                        rx.el.th(
                            "Price",
                            class_name="text-right text-sm font-semibold text-gray-600 p-3",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        CategoryState.selected_category_products,
                        lambda p: rx.el.tr(
                            rx.el.td(
                                p["title"],
                                class_name="p-3 text-sm text-gray-700 truncate max-w-sm",
                            ),
                            rx.el.td(
                                f"${p['numeric_price'].to_string()}",
                                class_name="p-3 text-sm text-gray-800 text-right font-medium",
                            ),
                            class_name="border-b border-gray-100",
                        ),
                    )
                ),
            ),
            class_name="overflow-x-auto rounded-lg border border-gray-200 bg-white",
        ),
        rx.el.a(
            "View All Products in this Category",
            href=f"/products?category={CategoryState.selected_category}",
            class_name="mt-4 inline-block text-sm font-medium text-emerald-600 hover:underline",
        ),
        class_name="p-6 bg-gray-50/75 rounded-xl border mt-6",
    )