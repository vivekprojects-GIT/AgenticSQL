from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import os

# Load DB env variables
load_dotenv()

# Define input schema
class SchemaExtractorInput(BaseModel):
    include_columns: bool = Field(default=True, description="Whether to include column names for each table")

# Define the actual CrewAI Tool
class SchemaExtractorTool(BaseTool):
    name: str = "schema_extractor"
    description: str = (
        "Fetches and returns the structure of all tables in the connected PostgreSQL database. "
        "Optionally includes column names for each table."
    )
    args_schema: Type[BaseModel] = SchemaExtractorInput

    def _run(self, include_columns: bool = True) -> str:
        try:
            engine = create_engine(
                f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
            )
            inspector = inspect(engine)

            schema_map = {}
            for table_name in inspector.get_table_names():
                if include_columns:
                    columns = [col["name"] for col in inspector.get_columns(table_name)]
                    schema_map[table_name] = columns
                else:
                    schema_map[table_name] = "columns hidden"

            return schema_map
        except Exception as e:
            return {"error": str(e)}