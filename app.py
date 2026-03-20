from google.adk.agents import Agent
from orchestrator.research_pipeline import run_pipeline

agent = Agent(
    name="multi_agent_research_system",
    description="AI Research Assistant using multiple agents",
    instruction="""
You are an AI research assistant.

When a user asks a question, run the research pipeline
to gather information and generate a structured report.
""",
    tools=[run_pipeline],
)