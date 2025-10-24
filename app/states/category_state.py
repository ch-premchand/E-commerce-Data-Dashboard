import reflex as rx
from app.states.dashboard_state import DashboardState, Product
from typing import TypedDict, Any
import asyncio
from collections import defaultdict
import statistics
import json
import os
import google.genai as genai
import logging


class CategoryHealth(TypedDict):
    name: str
    product_count: int
    avg_price: float
    avg_discount: float
    avg_colors: float
    health_score: int


class CategoryState(rx.State):
    products: list[Product] = []
    selected_category: str | None = None
    ai_insights: dict[str, str] = {}
    is_loading_insights: bool = False

    @rx.event
    async def on_load(self):
        dashboard_state = await self.get_state(DashboardState)
        if not dashboard_state.products:
            pass
        self.products = dashboard_state.products

    @rx.var
    def all_categories(self) -> list[str]:
        """All unique categories from the full product list."""
        if not self.products:
            return []
        return sorted(list(set((p["category"] for p in self.products))))

    @rx.var
    def category_stats(self) -> list[dict[str, str | float | int]]:
        if not self.products:
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
        for p in self.products:
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
        return stats

    @rx.var
    def category_health_scores(self) -> list[CategoryHealth]:
        if not self.category_stats:
            return []
        stats = self.category_stats
        product_counts = [s["product_count"] for s in stats]
        avg_prices = [s["avg_price"] for s in stats]
        avg_discounts = [s["avg_discount"] for s in stats]
        avg_colors = [s["avg_colors"] for s in stats]
        max_product_count = max(product_counts) if product_counts else 1
        median_price = statistics.median(avg_prices) if avg_prices else 0
        max_colors = max(avg_colors) if avg_colors else 1

        @rx.event
        def normalize(value, max_value):
            return min(value / max_value, 1.0) if max_value > 0 else 0

        health_data = []
        for s in stats:
            product_score = normalize(s["product_count"], max_product_count) * 25
            price_dev = (
                abs(s["avg_price"] - median_price) / median_price
                if median_price > 0
                else 0
            )
            price_score = max(0, 1 - price_dev) * 25
            discount_score = 0
            if 10 <= s["avg_discount"] <= 30:
                discount_score = 25
            elif 5 <= s["avg_discount"] < 10 or 30 < s["avg_discount"] <= 40:
                discount_score = 15
            color_score = normalize(s["avg_colors"], max_colors) * 25
            total_score = int(
                product_score + price_score + discount_score + color_score
            )
            health_data.append(
                {
                    "name": s["name"],
                    "product_count": s["product_count"],
                    "avg_price": s["avg_price"],
                    "avg_discount": s["avg_discount"],
                    "avg_colors": s["avg_colors"],
                    "health_score": total_score,
                }
            )
        return sorted(health_data, key=lambda x: x["health_score"], reverse=True)

    @rx.var
    def selected_category_data(self) -> CategoryHealth | None:
        if self.selected_category:
            for cat in self.category_health_scores:
                if cat["name"] == self.selected_category:
                    return cat
        return None

    @rx.var
    def selected_category_products(self) -> list[Product]:
        if not self.selected_category:
            return []
        return sorted(
            [p for p in self.products if p["category"] == self.selected_category],
            key=lambda p: p["numeric_price"],
            reverse=True,
        )[:10]

    @rx.event
    def select_category(self, category_name: str):
        if self.selected_category == category_name:
            self.selected_category = None
            self.ai_insights = {}
        else:
            self.selected_category = category_name
            self.ai_insights = {}

    @rx.event(background=True)
    async def generate_category_insights(self):
        if not self.selected_category_data:
            return
        async with self:
            self.is_loading_insights = True
            self.ai_insights = {}
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not set")
            client = genai.Client(api_key=api_key)
            async with self:
                category_data = self.selected_category_data
            prompt = f'You are an expert e-commerce strategist. Analyze the following category data and provide actionable insights.\n\n            **Category Data:**\n            {json.dumps(category_data, indent=2)}\n\n            Based on this data, provide a concise analysis in the following JSON format. Use Markdown for formatting within the strings.\n\n            {{\n                "pricing_strategy": "Is this category overpriced, underpriced, or well-priced? Suggest a pricing adjustment if necessary.",\n                "market_positioning": "Describe the market position. Is it premium, budget, or mid-range? Are there competitive gaps or opportunities?",\n                "inventory_optimization": "Based on its health score and metrics, should we expand, reduce, or maintain inventory for this category?",\n                "growth_opportunities": "Identify one key growth opportunity for this category. Be specific and actionable."\n            }}\n            '
            response = await client.models.generate_content_async(
                model="gemini-2.0-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )
            insights_raw = json.loads(response.text)
            insights = (
                insights_raw[0] if isinstance(insights_raw, list) else insights_raw
            )
            async with self:
                self.ai_insights = insights
        except Exception as e:
            logging.exception(f"Error generating category insights: {e}")
            async with self:
                self.ai_insights = {
                    "error": "Could not generate insights. Please check API key and try again."
                }
        finally:
            async with self:
                self.is_loading_insights = False