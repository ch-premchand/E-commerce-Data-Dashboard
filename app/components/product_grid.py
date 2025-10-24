import reflex as rx
from app.states.product_state import ProductState, Product


def product_card(product: Product) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src="/placeholder.svg",
                class_name="w-full h-48 object-cover rounded-t-lg",
            ),
            class_name="bg-gray-100 rounded-t-lg",
        ),
        rx.el.div(
            rx.el.span(
                product["category"],
                class_name="px-2 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800",
            ),
            rx.el.h3(
                product["title"],
                class_name="font-semibold text-gray-800 truncate mt-2 h-10",
            ),
            rx.el.div(
                rx.el.p(
                    f"${product['numeric_price'].to_string()}",
                    class_name="text-lg font-bold text-gray-900",
                ),
                rx.cond(
                    product["discount_value"] > 0,
                    rx.el.span(
                        f"{product['discount_value'].to_string()}% off",
                        class_name="px-2 py-1 text-xs font-bold rounded-full bg-red-100 text-red-800",
                    ),
                    rx.el.span(),
                ),
                class_name="flex items-center justify-between mt-2",
            ),
            class_name="p-4 flex-1 flex flex-col justify-between",
        ),
        class_name="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-lg transition-shadow duration-200 flex flex-col justify-between",
    )


def product_grid() -> rx.Component:
    return rx.cond(
        ProductState.paginated_products.length() > 0,
        rx.el.div(
            rx.foreach(ProductState.paginated_products, product_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
        ),
        rx.el.div(
            rx.el.p("No products match the current filters."),
            class_name="col-span-full text-center p-8 border rounded-lg bg-gray-50",
        ),
    )


def product_list_view() -> rx.Component:
    return rx.el.div(
        rx.el.p("List view will be implemented here."),
        class_name="text-center p-8 border rounded-lg bg-gray-50",
    )


def product_view_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                placeholder="Search products...",
                on_change=ProductState.set_search_query.debounce(300),
                default_value=ProductState.search_query,
                class_name="w-full md:w-64 pl-4 pr-4 py-2 border rounded-lg text-sm",
            ),
            rx.el.select(
                rx.el.option("Default Sort", value="default"),
                rx.el.option("Price: Low to High", value="price_asc"),
                rx.el.option("Price: High to Low", value="price_desc"),
                rx.el.option("Biggest Discount", value="discount_desc"),
                rx.el.option("Name (A-Z)", value="name_asc"),
                rx.el.option("Most Colors", value="colors_desc"),
                value=ProductState.sort_by,
                on_change=ProductState.set_sort_by,
                class_name="w-full md:w-auto pl-3 pr-10 py-2 border rounded-lg text-sm",
            ),
            class_name="flex flex-col md:flex-row gap-4",
        ),
        rx.el.div(
            rx.el.p(f"{ProductState.filtered_products.length()} results"),
            rx.el.button(
                rx.icon("grid-3x3"),
                on_click=ProductState.set_view_mode("grid"),
                class_name=rx.cond(
                    ProductState.view_mode == "grid",
                    "p-2 rounded-lg bg-emerald-100 text-emerald-600",
                    "p-2 rounded-lg bg-gray-100 text-gray-500 hover:bg-gray-200",
                ),
            ),
            rx.el.button(
                rx.icon("list"),
                on_click=ProductState.set_view_mode("list"),
                class_name=rx.cond(
                    ProductState.view_mode == "list",
                    "p-2 rounded-lg bg-emerald-100 text-emerald-600",
                    "p-2 rounded-lg bg-gray-100 text-gray-500 hover:bg-gray-200",
                ),
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex flex-col md:flex-row justify-between items-center mb-4 gap-4",
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=ProductState.set_current_page(ProductState.current_page - 1),
                disabled=ProductState.current_page <= 1,
                class_name="px-4 py-2 text-sm font-medium rounded-md border bg-white hover:bg-gray-50 disabled:opacity-50",
            ),
            rx.el.p(f"Page {ProductState.current_page} of {ProductState.total_pages}"),
            rx.el.button(
                "Next",
                on_click=ProductState.set_current_page(ProductState.current_page + 1),
                disabled=ProductState.current_page >= ProductState.total_pages,
                class_name="px-4 py-2 text-sm font-medium rounded-md border bg-white hover:bg-gray-50 disabled:opacity-50",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex justify-center mt-6",
    )