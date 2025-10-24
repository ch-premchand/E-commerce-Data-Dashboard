import reflex as rx
from app.components.sidebar import sidebar


def page_header(title: str) -> rx.Component:
    return rx.el.header(
        rx.el.h1(title, class_name="text-2xl font-bold tracking-tight text-gray-800"),
        class_name="flex items-center h-16 border-b px-6 shrink-0 bg-white z-10",
    )


def main_layout(page_content: rx.Component, title: str) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            page_header(title=title),
            rx.el.main(
                page_content, class_name="flex-1 p-6 bg-gray-50/50 overflow-y-auto"
            ),
            class_name="flex flex-col flex-1 max-h-screen",
        ),
        class_name="flex min-h-screen w-full font-['Montserrat'] bg-white",
    )