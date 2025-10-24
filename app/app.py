import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.navigation_state import NavigationState
from app.pages.dashboard import dashboard_page
from app.pages.products import products_page
from app.pages.categories import categories_page
from app.pages.ai_hub import ai_hub_page
from app.pages.reports import reports_page

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
app.add_page(
    dashboard_page,
    route="/",
    on_load=DashboardState.load_data,
    title="Dashboard Overview",
)
from app.states.product_state import ProductState

app.add_page(
    products_page,
    route="/products",
    title="Products Explorer",
    on_load=[DashboardState.load_data, ProductState.on_load],
)
from app.states.category_state import CategoryState

app.add_page(
    categories_page,
    route="/categories",
    title="Category Analytics",
    on_load=[DashboardState.load_data, CategoryState.on_load],
)
app.add_page(
    ai_hub_page, route="/ai-hub", title="AI Hub", on_load=DashboardState.load_data
)
app.add_page(
    reports_page, route="/reports", title="Reports", on_load=DashboardState.load_data
)