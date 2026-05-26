from olostep import Olostep
from app.config.settings import Settings
from app.agent.instruction.instructions import MANAGER_AGENT_INSTRUCTIONS, JUDGE_AGENT_INSTRUCTIONS, ANALYST_AGENT_INSTRUCTIONS
from agents import Agent
from app.model.research_models import ResearchReport, Judgement, MarkdownResearchReport
from typing import Any

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
def get_manager_agent(tools: list) -> Agent:
    name: str = "Manager Agent"
    return _create_agent(name, MANAGER_AGENT_INSTRUCTIONS, tools, ResearchReport)
    
""" create and return judge agent. """
def get_judge_agent() -> Agent:
    name: str = "Judge Agent"
    return _create_agent(name, JUDGE_AGENT_INSTRUCTIONS, [], Judgement)

def get_analyst_agent() -> Agent:
    name: str = "Analyst Agent"
    return _create_agent(name, ANALYST_AGENT_INSTRUCTIONS, [], MarkdownResearchReport)

def normalize_search_links(
    links: list[dict[str, Any]], limit: int = 8
) -> list[dict[str, Any]]:
    rows = []
    for link in links[:limit]:
        markdown = link.get("markdown_content") or ""
        rows.append(
            {
                "title": link.get("title") or "Untitled",
                "url": link.get("url") or "",
                "description": link.get("description") or "",
                "markdown_chars": len(markdown),
                "markdown_preview": markdown[:1500] if markdown else "",
            }
        )
    return rows
    
""" create an Agent """
def _create_agent(name, instructions: str, tools: list, output_type: Any) -> Agent:
    return Agent(
        name=name,
        tools=tools,
        instructions=instructions,
        model="gpt-5.4-mini",
        output_type=output_type
    )