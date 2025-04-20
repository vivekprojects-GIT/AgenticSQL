#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agsql.crew import Agsql

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': ''' i want an avg of total sales of kumar and  his arketing types?
            'Schema:
            Table: sales_data
            - id (INTEGER)
            - campaign_id (INTEGER)
            - total_sales (FLOAT)
            - salesDate(DATE)
            Foreign Keys:
            - campaign_id → marketing_campaigns.id

            Table: marketing_campaigns
            - id (INTEGER)
            - campaign_type (TEXT)
            - channel (TEXT)'''
        '',
        'current_year': str(datetime.now().year)
    }
    
    try:
        Agsql().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         Agsql().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Agsql().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
#     try:
#         Agsql().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
