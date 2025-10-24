import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.sidebar import sidebar
from app.components.kpi import kpi_grid, loading_skeleton
from app.components.charts import (
    charts_grid,
    top_products_table,
    charts_loading_skeleton,
)
from app.components.filters import filters_section


def dashboard_header() -> rx.Component:
    return rx.el.header(
        rx.el.h1(
            "E-Commerce Analytics Dashboard",
            class_name="text-2xl font-bold tracking-tight text-gray-800",
        ),
        class_name="flex items-center h-16 border-b px-6 shrink-0 bg-white",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            dashboard_header(),
            rx.el.main(
                rx.el.div(
                    filters_section(),
                    rx.cond(DashboardState.is_loading, loading_skeleton(), kpi_grid()),
                    rx.cond(
                        DashboardState.is_loading,
                        charts_loading_skeleton(),
                        rx.el.div(
                            charts_grid(), top_products_table(), class_name="space-y-6"
                        ),
                    ),
                    class_name="space-y-6",
                ),
                class_name="flex-1 p-6 bg-gray-50/50",
            ),
            class_name="flex flex-col flex-1",
        ),
        on_mount=DashboardState.load_data,
        class_name="flex min-h-screen w-full font-['Montserrat'] bg-white",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)