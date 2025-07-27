"""Academic_newresearch_agent for finding new research lines"""

from google.adk import Agent

from . import prompt

MODEL = "gemini-2.5-flash"

proxy = Agent(
    model=MODEL,
    name="proxy_agent",
    instruction=prompt.proxy_PROMPT,
)
