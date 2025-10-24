import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.kpi import kpi_grid, loading_skeleton
from app.components.charts import (
    charts_grid,
    top_products_table,
    charts_loading_skeleton,
)
from app.components.filters import filters_section
from app.components.analysis_panel import analysis_panel
from app.components.layout import main_layout


def dashboard_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            filters_section(),
            rx.cond(
                DashboardState.is_loading,
                rx.el.div(
                    loading_skeleton(),
                    charts_loading_skeleton(),
                    class_name="space-y-6",
                ),
                rx.el.div(
                    rx.el.div(
                        kpi_grid(),
                        charts_grid(),
                        top_products_table(),
                        class_name="space-y-6 flex-1",
                    ),
                    analysis_panel(),
                    class_name="grid lg:grid-cols-3 gap-6 items-start",
                ),
            ),
            class_name="space-y-6",
        ),
        title="Dashboard Overview",
    )