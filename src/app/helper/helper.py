from olostep import Olostep
from app.config.settings import Settings
from app.agent.instruction.instructions import MANAGER_INSTRUCTIONS, JUDGE_INSTRUCTIONS
from app.research.agent_tools import Toolset
from agents import Agent
from app.model.research_models import ResearchReport, Judgement

import json

def get_olostep_client(settings: Settings) -> Olostep:
    return Olostep(api_key=settings.olostep_api_key)

def convert_to_json_string(resp: dict, max_chars: int = 5000) -> str:
    data = {key: value for key,value in resp.items() if not key.startswith("_")}
    text = json.dumps(
        obj=data,
        ensure_ascii=False,
        indent=2
    )

    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n... [truncated]"

""" create and return manager/orchestrator agent. """
def get_manager_agent(self, tool_set: Toolset) -> Agent:
    name: str = "Manager Agent"
    tools: dict = [
        tool_set.answer_query,
        tool_set.judge_answer_quality,
        tool_set.search_with_scrape,
        tool_set.search_web,
        tool_set.scrape_url,
        analyst_tool
    ]
    return self._create_agent(name, MANAGER_INSTRUCTIONS, tools, ResearchReport)
    
""" create and return judge agent. """
def get_judge_agent(self) -> Agent:
    name: str = "Judge Agent"
    return self._create_agent(name, JUDGE_INSTRUCTIONS, None, Judgement)
    
""" create an Agent """
def _create_agent(self, name, instructions: str, tools: dict | None, output_type: any) -> Agent:
    return Agent(
        name=name,
        tools=tools,
        instructions=instructions,
        model="gpt-5.4-mini",
        output_type=output_type
    )