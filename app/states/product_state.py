import reflex as rx
from app.states.dashboard_state import DashboardState, Product
from typing import Literal
import asyncio
from collections import defaultdict

SortOptions = Literal[
    "default", "price_asc", "price_desc", "discount_desc", "name_asc", "colors_desc"
]


class ProductState(rx.State):
    products: list[Product] = []
    view_mode: Literal["grid", "list"] = "grid"
    sort_by: SortOptions = "default"
    search_query: str = ""
    selected_categories: list[str] = []
    price_range: list[float] = [0, 500]
    show_discounts_only: bool = False
    wishlist: set[str] = set()
    compare_products: set[str] = set()
    items_per_page: int = 24
    current_page: int = 1
    show_product_modal: bool = False
    selected_product: Product | None = None
    show_compare_modal: bool = False
    ai_recommendations: list[dict] = []
    is_loading_recommendations: bool = False

    @rx.event
    async def on_load(self):
        dashboard_state = await self.get_state(DashboardState)
        self.products = dashboard_state.products
        if self.products:
            max_price = max((p["numeric_price"] for p in self.products), default=500)
            self.price_range = [0, max_price]

    @rx.var
    def filtered_products(self) -> list[Product]:
        """Products filtered by search, category, price, and discounts."""
        filtered = self.products
        if self.search_query:
            filtered = [
                p for p in filtered if self.search_query.lower() in p["title"].lower()
            ]
        if self.selected_categories:
            filtered = [
                p for p in filtered if p["category"] in self.selected_categories
            ]
        if self.price_range[0] > 0 or self.price_range[1] < self.max_price:
            filtered = [
                p
                for p in filtered
                if self.price_range[0] <= p["numeric_price"] <= self.price_range[1]
            ]
        if self.show_discounts_only:
            filtered = [p for p in filtered if p["discount_value"] > 0]
        return filtered

    @rx.var
    def sorted_products(self) -> list[Product]:
        """Filtered products sorted based on the selected criteria."""
        products = self.filtered_products
        if self.sort_by == "price_asc":
            return sorted(products, key=lambda p: p["numeric_price"])
        if self.sort_by == "price_desc":
            return sorted(products, key=lambda p: p["numeric_price"], reverse=True)
        if self.sort_by == "discount_desc":
            return sorted(products, key=lambda p: p["discount_value"], reverse=True)
        if self.sort_by == "name_asc":
            return sorted(products, key=lambda p: p["title"])
        if self.sort_by == "colors_desc":
            return sorted(products, key=lambda p: p["color_count"], reverse=True)
        return products

    @rx.var
    def paginated_products(self) -> list[Product]:
        """The products to display on the current page."""
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_products[start:end]

    @rx.var
    def total_pages(self) -> int:
        """The total number of pages."""
        return -(-len(self.filtered_products) // self.items_per_page)

    @rx.var
    def all_categories(self) -> list[str]:
        """All unique categories from the full product list."""
        return sorted(list(set((p["category"] for p in self.products))))

    @rx.var
    def category_counts(self) -> dict[str, int]:
        """Count of products per category in the full list."""
        counts = defaultdict(int)
        for p in self.products:
            counts[p["category"]] += 1
        return counts

    @rx.var
    def max_price(self) -> float:
        if not self.products:
            return 500.0
        return max((p["numeric_price"] for p in self.products), default=500.0)

    @rx.var
    def wishlist_count(self) -> int:
        return len(self.wishlist)

    @rx.var
    def compare_count(self) -> int:
        return len(self.compare_products)

    @rx.var
    def active_filter_count(self) -> int:
        count = 0
        if self.search_query:
            count += 1
        if self.selected_categories:
            count += len(self.selected_categories)
        if self.price_range[0] > 0 or self.price_range[1] < self.max_price:
            count += 1
        if self.show_discounts_only:
            count += 1
        return count

    @rx.event
    def set_view_mode(self, mode: Literal["grid", "list"]):
        self.view_mode = mode

    @rx.event
    def set_sort_by(self, sort_option: SortOptions):
        self.sort_by = sort_option

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1

    @rx.event
    def toggle_category_filter(self, category: str):
        if category in self.selected_categories:
            self.selected_categories.remove(category)
        else:
            self.selected_categories.append(category)
        self.current_page = 1

    @rx.event
    def set_price_range(self, pr: list[float]):
        self.price_range = pr
        self.current_page = 1

    @rx.event
    def toggle_discount_filter(self, checked: bool):
        self.show_discounts_only = checked
        self.current_page = 1

    @rx.event
    def toggle_wishlist(self, product_title: str):
        if product_title in self.wishlist:
            self.wishlist.remove(product_title)
        else:
            self.wishlist.add(product_title)

    @rx.event
    def toggle_compare(self, product_title: str):
        if product_title in self.compare_products:
            self.compare_products.remove(product_title)
        elif len(self.compare_products) < 4:
            self.compare_products.add(product_title)

    @rx.event
    def clear_compare(self):
        self.compare_products = set()

    @rx.event
    def set_items_per_page(self, count: int):
        self.items_per_page = int(count)
        self.current_page = 1

    @rx.event
    def set_current_page(self, page_num: int):
        self.current_page = int(page_num)

    @rx.event
    def open_product_modal(self, product: Product):
        self.selected_product = product
        self.show_product_modal = True

    @rx.event
    def close_product_modal(self):
        self.show_product_modal = False
        self.selected_product = None

    @rx.event
    def open_compare_modal(self):
        self.show_compare_modal = True

    @rx.event
    def close_compare_modal(self):
        self.show_compare_modal = False

    @rx.event
    def clear_all_filters(self):
        self.search_query = ""
        self.selected_categories = []
        self.price_range = [0, self.max_price]
        self.show_discounts_only = False
        self.current_page = 1

    @rx.event(background=True)
    async def generate_recommendations(self, product: Product):
        async with self:
            self.is_loading_recommendations = True
            self.ai_recommendations = []
        await asyncio.sleep(2)
        async with self:
            similar_products = [
                p
                for p in self.products
                if p["category"] == product["category"]
                and p["title"] != product["title"]
            ][:5]
            recommendations = []
            for p in similar_products:
                recommendations.append(
                    {
                        "title": p["title"],
                        "reason": f"Similar style in the {p['category']} category.",
                    }
                )
            self.ai_recommendations = recommendations
            self.is_loading_recommendations = False