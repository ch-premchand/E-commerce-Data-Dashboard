import reflex as rx
from app.states.category_state import CategoryState, CategoryHealth


def health_score_badge(score: rx.Var[int]) -> rx.Component:
    color_class = rx.match(
        score.to_string(),
        *[(str(i), "bg-red-100 text-red-800") for i in range(50)],
        *[(str(i), "bg-yellow-100 text-yellow-800") for i in range(50, 80)],
        *[(str(i), "bg-emerald-100 text-emerald-800") for i in range(80, 101)],
        "bg-gray-100 text-gray-800",
    )
    return rx.el.div(
        rx.el.span("Health:"),
        rx.el.span(score),
        class_name=rx.el.span(
            "flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full ",
            color_class,
        ),
    )


def category_card(category: CategoryHealth) -> rx.Component:
    is_selected = CategoryState.selected_category == category["name"]
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon("tag", class_name="h-5 w-5 text-gray-500"),
                rx.el.h3(
                    category["name"], class_name="font-semibold text-gray-800 truncate"
                ),
                class_name="flex items-center gap-2",
            ),
            health_score_badge(category["health_score"]),
            class_name="flex items-center justify-between mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(category["product_count"], class_name="font-semibold text-lg"),
                rx.el.p("Products", class_name="text-xs text-gray-500"),
            ),
            rx.el.div(
                rx.el.p(
                    f"${category['avg_price']}", class_name="font-semibold text-lg"
                ),
                rx.el.p("Avg. Price", class_name="text-xs text-gray-500"),
            ),
            rx.el.div(
                rx.el.p(
                    f"{category['avg_discount']}%", class_name="font-semibold text-lg"
                ),
                rx.el.p("Avg. Discount", class_name="text-xs text-gray-500"),
            ),
            rx.el.div(
                rx.el.p(category["avg_colors"], class_name="font-semibold text-lg"),
                rx.el.p("Avg. Colors", class_name="text-xs text-gray-500"),
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-3 text-center",
        ),
        on_click=lambda: CategoryState.select_category(category["name"]),
        class_name=rx.cond(
            is_selected,
            "w-full p-4 bg-white rounded-xl border-2 border-emerald-500 shadow-lg text-left transition-all",
            "w-full p-4 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-gray-300 text-left transition-all",
        ),
    )


def category_overview_cards() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Category Overview", class_name="text-xl font-bold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.foreach(CategoryState.category_health_scores, category_card),
            class_name="grid md:grid-cols-2 lg:grid-cols-3 gap-4",
        ),
        class_name="p-6 bg-gray-50/75 rounded-xl border",
    )