import os
import sys

from crewai import Agent, Crew, Process, Task ,LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from agsql.tools.SchemaExtractorTool import SchemaExtractorTool
from agsql.tools.NaturalTimeParserDEFAULTTool import NaturalTimeParserTool


tool = SchemaExtractorTool()
schema_dict = tool._run()

# # Step 2: Format it into a string
# formatted_schema = ""
# for table, columns in schema_dict.items():
#     formatted_schema += f"\nTable: {table}\n" + "\n".join(f"- {col}" for col in columns)





# Step 3: Use it as a knowledge source
#product_specs = StringKnowledgeSource(content=formatted_schema )

load_dotenv()
# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# product_specs = StringKnowledgeSource(
#     content=,           # your schema string here
#     embedding_function=None             # 🚫 No embeddings
# )


#from agsql.tools.natural_time_parser import NaturalTimeParserTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# Create agent-specific knowledge about a product
# product_specs = StringKnowledgeSource(
#     embedding_function=None,
#     content="""
# Schema:
# Table: sales_data
# - id (INTEGER)
# - campaign_id (INTEGER)
# - total_sales (FLOAT)
# - salesDate(DATE)
# Foreign Keys:
# - campaign_id → marketing_campaigns.id

# Table: marketing_campaigns
# - id (INTEGER)
# - campaign_type (TEXT)
# - channel (TEXT)
#"""
# )


@CrewBase
class Agsql():

    ollama_llm = LLM(
        model="ollama/llama3.1:8b",
        api_base="http://localhost:11434",
        provider="ollama",
        temperature=0,
        complete_response=True,
        # max_tokens=2048
    )
    """Agsql crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def ner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ner_agent'],
            verbose=True,
            llm=self.ollama_llm
        )

    @agent
    def schema_mapper_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['schema_mapper_agent'],
            verbose=True,
            llm=self.ollama_llm,
            #knowledge_sources=[product_specs]
        )

    @agent
    def time_filter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['time_filter_agent'],
            tools=[NaturalTimeParserTool()],
            verbose=True,
            llm=self.ollama_llm
        )


    @agent
    def column_normalizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['column_normalizer_agent'],
            tools=[],
            verbose=True,
            llm=self.ollama_llm
        )

    @agent
    def sql_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_generator_agent'],
            tools=[],
            verbose=True,
            llm=self.ollama_llm
        )



    # @agent
    # def reporting_analyst(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['reporting_analyst'],
    #         verbose=True
    #     )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def ner_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['ner_extraction_task'],
            output_file='1NER.json'
        )


    @task
    def schema_mapping_task(self) -> Task:
        return Task(
            config=self.tasks_config['schema_mapping_task'],
            output_file='2SchemaMAP.json'
        )

    @task
    def resolve_time_filter_task(self) -> Task:
        return Task(
            config=self.tasks_config['resolve_time_filter_task'],
            output_file='3stepTimefilter.json'
        )

    @task
    def normalize_columns_task(self) -> Task:
        return Task(
            config=self.tasks_config['normalize_columns_task'],
            output_file='4stepnormalize.json'
        )

    @task
    def generate_sql_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_sql_task'],
            output_file='5generate_sql.json'
        )

    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['reporting_task'],
    #         output_file='report.md'
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the Agsql crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
