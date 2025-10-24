import reflex as rx
from app.states.dashboard_state import DashboardState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "border_color": "#E8E8E8",
        "border_radius": "0.75rem",
        "box_shadow": "0 2px 8px rgba(0,0,0,0.1)",
        "font_family": "'Montserrat', sans-serif",
        "font_size": "12px",
    },
    "cursor": {"stroke": "#A0A0A0", "stroke_width": 1, "stroke_dasharray": "3 3"},
}


def chart_card(title: str, chart: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-800 mb-4"),
        rx.el.div(chart, class_name="h-72"),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def chart_skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="h-6 bg-gray-200 rounded w-1/2 mb-4"),
        rx.el.div(class_name="h-72 bg-gray-200 rounded-lg"),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm animate-pulse",
    )


def charts_loading_skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            chart_skeleton(), chart_skeleton(), class_name="grid md:grid-cols-2 gap-6"
        ),
        rx.el.div(
            chart_skeleton(), chart_skeleton(), class_name="grid md:grid-cols-2 gap-6"
        ),
        rx.el.div(
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm animate-pulse h-96"
        ),
        class_name="space-y-6",
    )


def charts_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            chart_card(
                "Average Price by Category",
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(vertical=False, stroke_dasharray="3 3"),
                    rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                    rx.recharts.x_axis(
                        data_key="name",
                        tick_line=False,
                        axis_line=False,
                        tick_margin=8,
                        font_size=12,
                        hide=True,
                    ),
                    rx.recharts.y_axis(
                        axis_line=False,
                        tick_line=False,
                        tick_margin=8,
                        font_size=12,
                        unit="$",
                    ),
                    rx.recharts.bar(
                        data_key="avg_price",
                        name="Average Price",
                        fill="#10b981",
                        radius=[4, 4, 0, 0],
                    ),
                    data=DashboardState.category_stats,
                    margin={"left": -20},
                ),
            ),
            chart_card(
                "Average Discount by Category",
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(vertical=False, stroke_dasharray="3 3"),
                    rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                    rx.recharts.x_axis(
                        data_key="name",
                        tick_line=False,
                        axis_line=False,
                        tick_margin=8,
                        font_size=12,
                        hide=True,
                    ),
                    rx.recharts.y_axis(
                        axis_line=False,
                        tick_line=False,
                        tick_margin=8,
                        font_size=12,
                        unit="%",
                    ),
                    rx.recharts.bar(
                        data_key="avg_discount",
                        name="Avg Discount",
                        fill="#f59e0b",
                        radius=[4, 4, 0, 0],
                    ),
                    data=DashboardState.category_stats,
                    margin={"left": -20},
                ),
            ),
            class_name="grid md:grid-cols-2 gap-6",
        ),
        rx.el.div(
            chart_card(
                "Products per Category",
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(vertical=False, stroke_dasharray="3 3"),
                    rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                    rx.recharts.x_axis(
                        data_key="name",
                        angle=-45,
                        text_anchor="end",
                        height=70,
                        tick_line=False,
                        axis_line=False,
                        tick_margin=8,
                        font_size=12,
                    ),
                    rx.recharts.y_axis(
                        axis_line=False, tick_line=False, tick_margin=8, font_size=12
                    ),
                    rx.recharts.bar(
                        data_key="product_count",
                        name="# Products",
                        fill="#3b82f6",
                        radius=[4, 4, 0, 0],
                    ),
                    data=DashboardState.category_stats,
                    margin={"left": -20, "bottom": 20},
                ),
            ),
            chart_card(
                "Average Color Variety",
                rx.recharts.line_chart(
                    rx.recharts.cartesian_grid(vertical=False, stroke_dasharray="3 3"),
                    rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                    rx.recharts.x_axis(
                        data_key="name",
                        tick_line=False,
                        axis_line=False,
                        tick_margin=8,
                        font_size=12,
                        hide=True,
                    ),
                    rx.recharts.y_axis(
                        axis_line=False, tick_line=False, tick_margin=8, font_size=12
                    ),
                    rx.recharts.line(
                        data_key="avg_colors",
                        name="Avg Colors",
                        type_="monotone",
                        stroke="#8b5cf6",
                        stroke_width=2,
                        dot=False,
                    ),
                    data=DashboardState.category_stats,
                    margin={"left": -20},
                ),
            ),
            class_name="grid md:grid-cols-2 gap-6",
        ),
        class_name="space-y-6",
    )


def top_products_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Top 10 Most Expensive Products",
            class_name="text-lg font-semibold text-gray-800 mb-4",
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
                            "Category",
                            class_name="text-left text-sm font-semibold text-gray-600 p-3",
                        ),
                        rx.el.th(
                            "Price",
                            class_name="text-right text-sm font-semibold text-gray-600 p-3",
                        ),
                        class_name="border-b border-gray-200",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.top_10_expensive_products,
                        lambda product: rx.el.tr(
                            rx.el.td(
                                product["title"],
                                class_name="p-3 text-sm text-gray-700 truncate max-w-sm",
                            ),
                            rx.el.td(
                                rx.el.span(
                                    product["category"],
                                    class_name="px-2 py-1 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800",
                                )
                            ),
                            rx.el.td(
                                f"${product['numeric_price'].to_string()}",
                                class_name="p-3 text-sm text-gray-800 text-right font-medium",
                            ),
                            class_name="border-b border-gray-100 hover:bg-gray-50",
                        ),
                    )
                ),
            ),
            class_name="overflow-x-auto rounded-lg border border-gray-200",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )