import reflex as rx
from app.states.navigation_state import NavigationState


def nav_item(label: str, icon: str, href: str) -> rx.Component:
    is_active = rx.State.router.page.path == href
    return rx.link(
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
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-emerald-50 px-3 py-2 transition-all group",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:bg-gray-100 group",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.link(
                rx.icon("bar-chart-2", class_name="h-6 w-6 text-emerald-600"),
                rx.el.span("E-Commerce Analytics", class_name="font-semibold ml-2"),
                href="/",
                class_name="flex h-16 items-center justify-center border-b px-6",
            ),
            rx.el.nav(
                nav_item("Dashboard", "home", "/"),
                nav_item("Products", "package", "/products"),
                nav_item("Categories", "tag", "/categories"),
                nav_item("AI Hub", "sparkles", "/ai-hub"),
                nav_item("Reports", "file-text", "/reports"),
                class_name="flex flex-col gap-1 p-4 text-sm font-medium",
            ),
            class_name="flex-1 overflow-auto",
        ),
        class_name="w-64 border-r bg-gray-50/75 flex flex-col flex-shrink-0",
    )