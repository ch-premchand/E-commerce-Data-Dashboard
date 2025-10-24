import reflex as rx
import os
import google.genai as genai
import logging
import json
from app.states.dashboard_state import DashboardState


class AnalysisState(rx.State):
    is_loading_analysis: bool = False
    analysis_content: dict[str, str] = {
        "trends": "",
        "recommendations": "",
        "anomalies": "",
        "opportunities": "",
    }

    @rx.event(background=True)
    async def generate_analysis(self):
        async with self:
            self.is_loading_analysis = True
            self.analysis_content = {
                "trends": "",
                "recommendations": "",
                "anomalies": "",
                "opportunities": "",
            }
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                logging.error("GOOGLE_API_KEY not found.")
                raise ValueError("API key is missing.")
            client = genai.Client(api_key=api_key)
            async with self:
                dashboard_state = await self.get_state(DashboardState)
                kpis = {
                    "Total Products": dashboard_state.total_products,
                    "Average Price": f"${dashboard_state.average_price:.2f}",
                    "Total Categories": dashboard_state.total_categories,
                    "Average Discount": f"{dashboard_state.average_discount:.2f}%",
                    "Products with Discounts": dashboard_state.products_with_discounts,
                    "Average Colors per Product": f"{dashboard_state.avg_colors:.1f}",
                }
                category_stats = dashboard_state.category_stats[:5]
                top_products = dashboard_state.top_10_expensive_products[:5]
            prompt = f'You are a professional e-commerce data analyst. Your task is to provide a concise, insightful analysis of the provided dashboard data. \n            The user has applied some filters, and this is the resulting dataset. Analyze the KPIs, category performance, and top products to identify key insights. \n            \n            **Dashboard Data Summary:**\n            - **Key Performance Indicators (KPIs):** {json.dumps(kpis, indent=2)}\n            - **Top 5 Category Statistics:** {json.dumps(category_stats, indent=2)}\n            - **Top 5 Most Expensive Products:** {json.dumps(top_products, indent=2)}\n\n            **Your Analysis (Strictly follow this JSON format and use Markdown for formatting within strings):**\n            {{\n                "trends": "Identify 1-2 key trends from the data. What patterns are emerging?",\n                "recommendations": "Provide 1-2 actionable business recommendations based on your analysis.",\n                "anomalies": "Point out any surprising or unusual data points that might require further investigation.",\n                "opportunities": "Highlight 1-2 potential opportunities for business growth or optimization."\n            }}\n            '
            response = await client.models.generate_content_async(
                model="gemini-2.0-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )
            analysis_data_raw = json.loads(response.text)
            analysis_data = (
                analysis_data_raw[0]
                if isinstance(analysis_data_raw, list)
                else analysis_data_raw
            )
            async with self:
                self.analysis_content = analysis_data
        except Exception as e:
            logging.exception(f"Error generating analysis: {e}")
            async with self:
                self.analysis_content["anomalies"] = (
                    "Sorry, there was an error generating the analysis. Please check the logs and try again."
                )
        finally:
            async with self:
                self.is_loading_analysis = False