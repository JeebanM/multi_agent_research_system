from google.adk.agents import Agent
from orchestrator.research_pipeline import run_pipeline

root_agent = Agent(
    name="multi_agent_research_system",
    description="AI research assistant",
    instruction="""
You are an AI research assistant.

When the user asks a question, run the research pipeline
to search sources, verify information, and generate a report.
""",
    tools=[run_pipeline],
)