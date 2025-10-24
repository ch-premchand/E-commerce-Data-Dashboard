import reflex as rx
import pandas as pd
import kagglehub
import os
import asyncio
import logging
from typing import TypedDict, Any
from collections import defaultdict


class Product(TypedDict):
    category: str
    title: str
    price_str: str
    numeric_price: float
    discount_str: str | None
    discount_value: float
    color_count: int
    selling_proposition: str | None


class DashboardState(rx.State):
    products: list[Product] = []
    is_loading: bool = True
    search_query: str = ""
    selected_categories: list[str] = []
    price_range: list[float] = [0, 500]
    show_discounts_only: bool = False

    @rx.event(background=True)
    async def load_data(self):
        async with self:
            if self.products:
                logging.info(f"Data already loaded: {len(self.products)} products.")
                self.is_loading = False
                return
            self.is_loading = True
            logging.info("Starting data load...")
        try:
            logging.info("Downloading dataset from Kagglehub...")
            path = kagglehub.dataset_download("oleksiimartusiuk/e-commerce-data-shein")
            files = [f for f in os.listdir(path) if f.endswith(".csv")]
            logging.info(f"Found {len(files)} CSV files to process.")
            all_products = []
            for i, file in enumerate(files, 1):
                try:
                    category_name = (
                        file.replace("us-shein-", "")
                        .replace(".csv", "")
                        .replace("_", " ")
                        .title()
                    )
                    df = pd.read_csv(os.path.join(path, file))
                    if "goods-title-link--jump" in df.columns:
                        df.rename(
                            columns={
                                "goods-title-link--jump": "title",
                                "goods-title-link": "title_alt",
                            },
                            inplace=True,
                        )
                        df["title"] = df["title"].fillna(df["title_alt"])
                    elif "goods-title-link" in df.columns:
                        df.rename(columns={"goods-title-link": "title"}, inplace=True)
                    else:
                        logging.warning(
                            f"Skipping file {file} due to missing title column."
                        )
                        continue
                    df = df.dropna(subset=["title", "price"])
                    for _, row in df.iterrows():
                        price_str = str(row.get("price", "0"))
                        numeric_price = 0.0
                        if isinstance(price_str, str):
                            price_cleaned = (
                                price_str.replace("$", "").replace(",", "").strip()
                            )
                            if "-" in price_cleaned:
                                parts = price_cleaned.split("-")
                                try:
                                    numeric_price = (
                                        float(parts[0].strip())
                                        + float(parts[1].strip())
                                    ) / 2
                                except (ValueError, IndexError) as e:
                                    logging.exception(
                                        f"Error parsing price range: {price_cleaned}, {e}"
                                    )
                                    numeric_price = 0.0
                            else:
                                try:
                                    numeric_price = float(price_cleaned)
                                except ValueError as e:
                                    logging.exception(
                                        f"Error parsing price: {price_cleaned}, {e}"
                                    )
                                    numeric_price = 0.0
                        discount_str = row.get("discount")
                        discount_value = 0.0
                        if pd.notna(discount_str) and isinstance(discount_str, str):
                            try:
                                discount_value = float(
                                    discount_str.replace("%", "").replace("-", "")
                                )
                            except ValueError as e:
                                logging.exception(
                                    f"Error parsing discount: {discount_str}, {e}"
                                )
                                discount_value = 0.0
                        color_count_raw = row.get("color-count")
                        color_count = (
                            int(color_count_raw)
                            if pd.notna(color_count_raw)
                            and str(color_count_raw).isdigit()
                            else 0
                        )
                        all_products.append(
                            {
                                "category": category_name,
                                "title": str(row.get("title", "No Title")),
                                "price_str": price_str,
                                "numeric_price": round(numeric_price, 2),
                                "discount_str": str(discount_str)
                                if pd.notna(discount_str)
                                else None,
                                "discount_value": discount_value,
                                "color_count": color_count,
                                "selling_proposition": str(
                                    row.get("selling_proposition")
                                )
                                if pd.notna(row.get("selling_proposition"))
                                else None,
                            }
                        )
                    if i % 5 == 0 or i == len(files):
                        logging.info(
                            f"Processed {i}/{len(files)} files ({len(all_products)} products so far)."
                        )
                except Exception as e:
                    logging.exception(f"Skipped file {file}: {e}")
            async with self:
                self.products = all_products
                logging.info(f"Data loaded successfully: {len(all_products)} products.")
                if all_products:
                    max_price = max(
                        (p["numeric_price"] for p in all_products), default=0
                    )
                    self.price_range = [0, max_price]
        except Exception as e:
            logging.exception(f"Failed to load data: {e}")
            async with self:
                self.products = []
        finally:
            async with self:
                self.is_loading = False
                logging.info(
                    f"Loading complete. is_loading = {self.is_loading}, products = {len(self.products)}."
                )

    @rx.var
    def total_products(self) -> int:
        return len(self.filtered_products)

    @rx.var
    def average_price(self) -> float:
        if not self.filtered_products:
            return 0.0
        total = sum(
            (
                p["numeric_price"]
                for p in self.filtered_products
                if p["numeric_price"] > 0
            )
        )
        count = sum((1 for p in self.filtered_products if p["numeric_price"] > 0))
        return round(total / count, 2) if count > 0 else 0.0

    @rx.var
    def total_categories(self) -> int:
        if not self.filtered_products:
            return 0
        return len(set((p["category"] for p in self.filtered_products)))

    @rx.var
    def average_discount(self) -> float:
        if not self.filtered_products:
            return 0.0
        discounted_products = [
            p for p in self.filtered_products if p["discount_value"] > 0
        ]
        if not discounted_products:
            return 0.0
        return round(
            sum((p["discount_value"] for p in discounted_products))
            / len(discounted_products),
            2,
        )

    @rx.var
    def products_with_discounts(self) -> int:
        return sum((1 for p in self.filtered_products if p["discount_value"] > 0))

    @rx.var
    def avg_colors(self) -> float:
        if not self.filtered_products:
            return 0.0
        products_with_colors = [
            p for p in self.filtered_products if p["color_count"] > 0
        ]
        if not products_with_colors:
            return 0.0
        return round(
            sum((p["color_count"] for p in products_with_colors))
            / len(products_with_colors),
            1,
        )

    @rx.var
    def category_stats(self) -> list[dict[str, str | int | float]]:
        if not self.filtered_products:
            return []
        category_data = defaultdict(
            lambda: {
                "price_sum": 0,
                "price_count": 0,
                "discount_sum": 0,
                "discount_count": 0,
                "product_count": 0,
                "color_sum": 0,
                "color_count": 0,
            }
        )
        for p in self.filtered_products:
            cat = p["category"]
            category_data[cat]["product_count"] += 1
            if p["numeric_price"] > 0:
                category_data[cat]["price_sum"] += p["numeric_price"]
                category_data[cat]["price_count"] += 1
            if p["discount_value"] > 0:
                category_data[cat]["discount_sum"] += p["discount_value"]
                category_data[cat]["discount_count"] += 1
            if p["color_count"] > 0:
                category_data[cat]["color_sum"] += p["color_count"]
                category_data[cat]["color_count"] += 1
        stats = []
        for category, data in category_data.items():
            stats.append(
                {
                    "name": category,
                    "avg_price": round(data["price_sum"] / data["price_count"], 2)
                    if data["price_count"] > 0
                    else 0,
                    "avg_discount": round(
                        data["discount_sum"] / data["discount_count"], 2
                    )
                    if data["discount_count"] > 0
                    else 0,
                    "product_count": data["product_count"],
                    "avg_colors": round(data["color_sum"] / data["color_count"], 1)
                    if data["color_count"] > 0
                    else 0,
                }
            )
        return sorted(stats, key=lambda x: x["name"])

    @rx.var
    def top_10_expensive_products(self) -> list[Product]:
        return sorted(
            self.filtered_products, key=lambda p: p["numeric_price"], reverse=True
        )[:10]

    @rx.var
    def all_categories(self) -> list[str]:
        return sorted(list(set((p["category"] for p in self.products))))

    @rx.var
    def max_price(self) -> float:
        if not self.products:
            return 1000.0
        return max((p["numeric_price"] for p in self.products)) or 1000.0

    @rx.var
    def filtered_products(self) -> list[Product]:
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
    def active_filter_count(self) -> int:
        count = 0
        if self.search_query:
            count += 1
        if self.selected_categories:
            count += 1
        if self.price_range[0] > 0 or self.price_range[1] < self.max_price:
            count += 1
        if self.show_discounts_only:
            count += 1
        return count

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_selected_categories_list(self, category: str):
        if not category:
            self.selected_categories = []
        else:
            self.selected_categories = [category]

    @rx.event
    def set_price_range(self, pr: list[float]):
        self.price_range = pr

    @rx.event
    def set_show_discounts_only(self, checked: bool):
        self.show_discounts_only = checked

    @rx.event
    def clear_filters(self):
        self.search_query = ""
        self.selected_categories = []
        self.price_range = [0, self.max_price]
        self.show_discounts_only = False