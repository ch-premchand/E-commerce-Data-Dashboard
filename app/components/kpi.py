import reflex as rx
from app.states.dashboard_state import DashboardState


def kpi_card(
    title: str,
    value: rx.Var[str | int | float],
    icon: str,
    icon_color: str,
    change: rx.Var[str] | None = None,
    change_color: str = "",
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(title, class_name="text-sm font-medium text-gray-500"),
            rx.icon(icon, class_name=f"h-5 w-5 {icon_color}"),
            class_name="flex items-center justify-between",
        ),
        rx.el.div(
            rx.el.p(value, class_name="text-3xl font-bold text-gray-800"),
            rx.cond(
                change,
                rx.el.p(change, class_name=f"text-xs {change_color}"),
                rx.el.div(),
            ),
            class_name="mt-2 flex items-baseline gap-2",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow duration-200",
    )


def kpi_grid() -> rx.Component:
    return rx.el.div(
        kpi_card(
            "Total Products",
            DashboardState.total_products,
            "package",
            "text-emerald-500",
        ),
        kpi_card(
            "Average Price",
            f"${DashboardState.average_price.to_string()}",
            "dollar-sign",
            "text-blue-500",
        ),
        kpi_card(
            "Total Categories",
            DashboardState.total_categories,
            "tag",
            "text-orange-500",
        ),
        kpi_card(
            "Average Discount",
            f"{DashboardState.average_discount.to_string()}%",
            "percent",
            "text-purple-500",
        ),
        kpi_card(
            "Products with Discounts",
            DashboardState.products_with_discounts,
            "trending-down",
            "text-red-500",
        ),
        kpi_card(
            "Avg Colors/Product",
            DashboardState.avg_colors.to_string(),
            "palette",
            "text-indigo-500",
        ),
        class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6",
    )


def loading_skeleton() -> rx.Component:
    def skeleton_card():
        return rx.el.div(
            rx.el.div(
                rx.el.div(class_name="h-4 bg-gray-200 rounded w-3/4"),
                rx.el.div(class_name="h-5 w-5 bg-gray-200 rounded-full"),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(
                rx.el.div(class_name="h-8 bg-gray-300 rounded w-1/2 mt-2"),
                class_name="mt-2",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm animate-pulse",
        )

    return rx.el.div(
        skeleton_card(),
        skeleton_card(),
        skeleton_card(),
        skeleton_card(),
        skeleton_card(),
        skeleton_card(),
        class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6",
    )