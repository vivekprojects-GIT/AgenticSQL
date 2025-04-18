from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import dateparser
from datetime import datetime


class NaturalTimeParserInput(BaseModel):
    time_phrase: str = Field(..., description="A natural language time expression like 'Q2', 'yesterday', or 'last 7 days'.")


class NaturalTimeParserTool(BaseTool):
    name: str = "natural_time_parser"
    description: str = (
        "Parses natural language time expressions such as 'today', 'yesterday', 'last 30 days', "
        "'Q1', or 'last week' into a structured date or date range using the current system date "
        "as reference. Useful for resolving vague or relative time references into precise filters "
        "for SQL queries, dashboards, and data reports."
    )
    args_schema: Type[BaseModel] = NaturalTimeParserInput

    def _run(self, time_phrase: str) -> dict:
        today = datetime.today()
        parsed = dateparser.parse(time_phrase, settings={'RELATIVE_BASE': today, 'PREFER_DATES_FROM': 'past'})
        if parsed:
            date_str = parsed.strftime("%Y-%m-%d")
            return {
                "start_date": date_str,
                "end_date": date_str
            }
        else:
            return {
                "error": f"Could not resolve time expression: {time_phrase}"
            }