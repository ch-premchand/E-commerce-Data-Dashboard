import reflex as rx
from app.states.analysis_state import AnalysisState


def insight_category(icon: str, title: str, content: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-gray-500"),
            rx.el.h4(title, class_name="font-semibold text-gray-700"),
            class_name="flex items-center gap-2",
        ),
        rx.el.div(
            rx.markdown(
                content,
                component_map={
                    "p": lambda text: rx.el.p(text, class_name="text-sm text-gray-600")
                },
            ),
            class_name="pl-7 prose prose-sm max-w-none text-gray-600",
        ),
        class_name="space-y-1",
    )


def analysis_loading_skeleton() -> rx.Component:
    def skeleton_item():
        return rx.el.div(
            rx.el.div(class_name="h-5 w-1/3 bg-gray-200 rounded-md"),
            rx.el.div(class_name="h-4 w-full bg-gray-200 rounded-md mt-2"),
            rx.el.div(class_name="h-4 w-5/6 bg-gray-200 rounded-md mt-1"),
        )

    return rx.el.div(
        rx.el.h3("Analyzing Data...", class_name="text-lg font-semibold text-gray-800"),
        rx.el.div(class_name="flex items-center text-sm text-gray-500 gap-2"),
        rx.el.div(
            skeleton_item(),
            skeleton_item(),
            skeleton_item(),
            class_name="space-y-6 animate-pulse mt-4",
        ),
    )


def analysis_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "AI-Powered Analysis", class_name="text-lg font-semibold text-gray-800"
            ),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-4 w-4 mr-2"),
                "Regenerate",
                on_click=AnalysisState.generate_analysis,
                class_name="flex items-center text-sm font-medium text-emerald-600 hover:text-emerald-800",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(
            "Insights based on the current filters.", class_name="text-sm text-gray-500"
        ),
        rx.el.div(
            insight_category(
                "trending-up", "Trends", AnalysisState.analysis_content["trends"]
            ),
            insight_category(
                "thumbs-up",
                "Recommendations",
                AnalysisState.analysis_content["recommendations"],
            ),
            insight_category(
                "flag_triangle_right",
                "Anomalies",
                AnalysisState.analysis_content["anomalies"],
            ),
            insight_category(
                "lightbulb",
                "Opportunities",
                AnalysisState.analysis_content["opportunities"],
            ),
            class_name="space-y-4 mt-4",
        ),
        class_name="space-y-1",
    )


def generate_analysis_button() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("sparkles", class_name="h-6 w-6 text-emerald-500"),
            class_name="p-3 bg-emerald-100 rounded-full",
        ),
        rx.el.h3(
            "Professional Analysis", class_name="text-lg font-semibold text-gray-800"
        ),
        rx.el.p(
            "Get AI-powered insights on your filtered data.",
            class_name="text-sm text-gray-500",
        ),
        rx.el.button(
            "Generate Analysis",
            rx.icon("arrow-right", class_name="ml-2 h-4 w-4"),
            on_click=AnalysisState.generate_analysis,
            class_name="mt-4 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500",
        ),
        class_name="text-center flex flex-col items-center justify-center space-y-2 h-full",
    )


def analysis_panel() -> rx.Component:
    return rx.el.div(
        rx.match(
            AnalysisState.is_loading_analysis.to_string(),
            ("True", analysis_loading_skeleton()),
            (
                "False",
                rx.cond(
                    AnalysisState.analysis_content["trends"] != "",
                    analysis_content(),
                    generate_analysis_button(),
                ),
            ),
        ),
        class_name="lg:col-span-1 bg-white p-6 rounded-xl border border-gray-200 shadow-sm lg:sticky lg:top-6 h-full min-h-[400px] flex flex-col justify-center",
    )