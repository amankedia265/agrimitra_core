
from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-flash"

websearch_agent = Agent(
    model=MODEL,
    name="websearch_agent",
    instruction=prompt.WEBSEARCH_PROMPT,
    output_key="questions",
    tools=[google_search],
)
