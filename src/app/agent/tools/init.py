from .answer_query import build_answer_query_tool
from .judge_answer_quality import build_judge_answer_quality_tool
from .search_with_scrape import build_search_with_scrape_tool
from .search_web import build_search_web_tool
from .scrape_url import build_scrape_url_tool
from .analyst_agent import build_analyst_agent_tool

from app.config.settings import Settings

def build_tools(settings: Settings):
    return[
        build_answer_query_tool(settings),
        build_judge_answer_quality_tool(),
        build_search_with_scrape_tool(settings),
        build_search_web_tool(settings),
        build_scrape_url_tool(settings),
        build_analyst_agent_tool()
    ]