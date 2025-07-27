"""Academic_Research: Research advice, related literature finding, research area proposals, web knowledge access."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
#from .sub_agents.academic_newresearch import academic_newresearch_agent
from .sub_agents.websearch_agent import websearch_agent
from .sub_agents.rag_agent import rag_agent
from .sub_agents.weather_forecast_agent import weather_forecast_agent
from .sub_agents.shopping_agent import shopping_agent
from .sub_agents.data_science.data_science.agent import root_agent as db_ds_multiagent



MODEL = "gemini-2.5-flash"


agrimitra_agent = LlmAgent(
    name="agrimitra_agent",
    model=MODEL,
    description=(
     """This is the central orchestrator agent that receives all farmer queries and routes them to the most relevant expert agent.
    It does not generate the final answer on its own but identifies the right sub-agent to handle the query. 
    It has access to agents for crop planning, fertilizer advice, pest and disease help, mandi prices, government schemes, weather forecasts, and farm task scheduling.
    """
    ),
    instruction=prompt.ROOT_FARMER_AGENT,
    output_key="seminal_paper",
    tools=[
        AgentTool(agent=websearch_agent),
        AgentTool(agent=rag_agent),
        AgentTool(agent=weather_forecast_agent),
        AgentTool(agent=shopping_agent),
        AgentTool(agent=db_ds_multiagent),
    ],
)

root_agent = agrimitra_agent