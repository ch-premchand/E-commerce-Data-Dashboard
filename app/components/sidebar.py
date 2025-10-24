import reflex as rx
from app.states.dashboard_state import DashboardState


def nav_item(label: str, icon: str, href: str) -> rx.Component:
    is_active = DashboardState.active_nav == label
    return rx.el.a(
        rx.icon(
            icon,
            class_name=rx.cond(
                is_active, "text-emerald-500", "text-gray-500 group-hover:text-gray-700"
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                is_active,
                "font-semibold text-gray-800",
                "text-gray-700 group-hover:text-gray-800",
            ),
        ),
        href=href,
        on_click=lambda: DashboardState.set_active_nav(label),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-emerald-50 px-3 py-2 transition-all group",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:bg-gray-100 group",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("bar-chart-2", class_name="h-6 w-6 text-emerald-600"),
                rx.el.span("E-Commerce Analytics", class_name="sr-only"),
                href="#",
                class_name="flex h-16 items-center justify-center",
            ),
            rx.el.nav(
                nav_item("Dashboard", "home", "#"),
                nav_item("Products", "package", "#"),
                nav_item("Categories", "tag", "#"),
                class_name="grid items-start px-4 text-sm font-medium",
            ),
            class_name="flex-1 overflow-auto py-2",
        ),
        class_name="border-r bg-gray-50/75 w-64 flex-shrink-0",
    )