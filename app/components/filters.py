import reflex as rx
from app.states.dashboard_state import DashboardState


def category_filter() -> rx.Component:
    return rx.el.div(
        rx.el.p("Category", class_name="text-sm font-medium text-gray-700 mb-2"),
        rx.el.div(
            rx.el.select(
                rx.el.option("All Categories", value=""),
                rx.foreach(
                    DashboardState.all_categories,
                    lambda category: rx.el.option(category, value=category),
                ),
                value=DashboardState.selected_categories.join(","),
                on_change=DashboardState.toggle_category,
                class_name="w-full pl-3 pr-10 py-2 border rounded-lg text-sm",
            ),
            class_name="relative w-full",
        ),
        class_name="w-full md:w-auto",
    )


def search_filter() -> rx.Component:
    return rx.el.div(
        rx.el.p("Search", class_name="text-sm font-medium text-gray-700 mb-2"),
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
            ),
            rx.el.input(
                placeholder="Search products...",
                on_change=DashboardState.set_search_query,
                class_name="w-full pl-10 pr-4 py-2 border rounded-lg text-sm",
                default_value=DashboardState.search_query,
            ),
            class_name="relative w-full",
        ),
        class_name="w-full md:w-auto",
    )


def discount_filter() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            rx.el.span(
                "Show only discounted items",
                class_name="text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                type="checkbox",
                checked=DashboardState.show_discounts_only,
                on_change=DashboardState.toggle_discount_filter,
                class_name="ml-2 h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500",
            ),
            class_name="flex items-center",
        )
    )


def clear_filters_button() -> rx.Component:
    return rx.el.button(
        "Clear Filters",
        rx.el.span(
            DashboardState.active_filter_count,
            class_name="ml-2 px-2 py-0.5 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800",
        ),
        on_click=DashboardState.clear_filters,
        class_name="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50",
        disabled=DashboardState.active_filter_count == 0,
    )


def filters_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(search_filter(), class_name="flex-1 min-w-[200px]"),
            rx.el.div(category_filter(), class_name="flex-1 min-w-[200px]"),
            class_name="grid md:grid-cols-2 gap-4",
        ),
        rx.el.div(
            discount_filter(),
            clear_filters_button(),
            class_name="flex flex-col md:flex-row items-center justify-between gap-4 pt-4 border-t border-gray-200 mt-4 md:mt-0 md:border-0 md:pt-0 md:gap-6",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-200 shadow-sm mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4",
    )