from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import dateparser
from datetime import datetime


# ✅ Input schema for the tool
class NaturalTimeParserInput(BaseModel):
    time_phrase: str = Field(
        ...,
        description="Natural time expression like 'today', 'last 30 days', 'Q2', 'yesterday', etc."
    )


# ✅ CrewAI-compatible tool class
class NaturalTimeParserTool(BaseTool):
    name: str = "natural_time_parser"
    description: str = (
        "Parses natural language time expressions such as 'today', 'yesterday', 'last 30 days', "
        "'Q1', or 'last week' into a structured date or date range using the current system date "
        "as reference. This tool helps agents convert vague or relative time references into "
        "precise start and end dates for use in time filtering, SQL generation, or analytics."
    )
    args_schema: Type[BaseModel] = NaturalTimeParserInput

    def _run(self, time_phrase: str) -> dict:
        today = datetime.today()
        parsed = dateparser.parse(time_phrase, settings={"RELATIVE_BASE": today})

        if parsed:
            date_str = parsed.strftime("%Y-%m-%d")
            return {
                "start_date": date_str,
                "end_date": date_str
            }

        return {
            "error": f"Could not resolve time expression: {time_phrase}"
        }