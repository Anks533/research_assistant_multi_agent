from openai import function_tool
from app.exception.exceptions import OlostepError
from agents import custom_span, Agent, Runner, RunResult
from app.config.settings import Settings
from app.helper.helper import get_olostep_client, convert_to_json_string, get_judge_agent, normalize_search_links
from olostep.models.response import AnswersResponse
from app.model.research_models import Judgement
from app.config.logging import get_logger

import asyncio
import logging

logger: logging.Logger = get_logger("Toolset")

class Toolset:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @function_tool
    async def answer_query(self, query: str) -> str:
        """Provide a simple initial answer without deep research using Olostep Answer API."""
        try:
            logger.debug("Invoking Answer API...")
            result = await asyncio.to_thread(self._answer_query_impl, query)
            logger.debug("Query Answer via Answer API :: \n")
            logger.debug(result)
        except Exception as ex:
            raise OlostepError(f"Olostep Answer API failed with exception : {ex}") from ex
        return result

    @function_tool
    async def judge_answer_quality(self, query: str, evidence: str, stage: str = "current evidence") -> str:
        """Judge whether the current answer is sufficient."""
        prompt = f"""
        Original Research Query:
        {query}

        Evidence stage:
        {stage}

        Evidence to judge:
        {evidence}

        Return a structured judgement against this evidence of original query whether it is sufficient. 
        """

        judge_agent: Agent = get_judge_agent()

        with custom_span("judge.answer.quality", {"stage": stage}):
            logger.debug("Starting Judge Agent...")
            result: RunResult = await Runner.run(judge_agent, prompt,max_turns=3)
            judgement: Judgement = result.final_output
            judgement_json = judgement.model_dump_json()
            logger.debug("Judge Agent completed...")
            logger.debug("Judgement:: \n")
            logger.debug(judgement_json)
        return judgement_json
        

    @function_tool
    async def search_with_scrape(self, query: str, limit: int = 5) -> list:
        """Search the web and scrape relevant sources."""
        try:
            logger.debug("Search API Invoked....")
            result = await asyncio.to_thread(self._search_with_scrape_impl, query, limit)
            logger.debug("Search API Completed....")
            logger.debug("Search Result :: \n")
            logger.debug(result)
        except Exception as exc:
            raise OlostepError(f"Olostep Search with Scrape failed: {exc}") from exc
        return result

        
    @function_tool
    async def search_web(self, query: str, limit: int = 8) -> list:
        """Search the web using Olostep Search and return normalized results."""
        try:
            result = await asyncio.to_thread(self._search_web_impl, query, limit)
        except Exception as exc:
            raise OlostepError(f"Olostep Search API failed: {exc}") from exc
        return result

    @function_tool
    async def scrape_url(self, url: str) -> str:
        """Scrape one URL with Olostep and return compact page content."""
        try:
            result = await asyncio.to_thread(self._scrape_url_impl, url)
        except Exception as exc:
            raise OlostepError(f"Olostep Scrape API failed: {exc}") from exc
        return result


    """ call Answer api and return json string response. """
    def _answer_query_impl(self, query: str) -> str:
        with custom_span(
            name = "olostep.answer_query",
            data = {
                "query": query
            }
        ):
            result: AnswersResponse = get_olostep_client(self.settings).answers.create(task=query)
            result_dict: dict = vars(result)
            return convert_to_json_string(result_dict)
        
    def _search_with_scrape_impl(self, query: str, limit: int = 5) -> str:
        scrape_options = {"formats":["markdown"], "timeout": 25}
        with custom_span("olostep.search_with_scrape", {"query": query, "limit": limit, "scrape_options": scrape_options}):
            search = get_olostep_client().searches.create(
                query=query,
                limit=limit,
                scrape_options=scrape_options
            )
            data = {key: value for key, value in vars(search).items() if not key.startswith("_")}
            return convert_to_json_string({
                "query": query,
                "results": normalize_search_links(data.get("links", []), limit=limit),
                "raw": data
            }, max_chars=12000)
    
    def _scrape_url_impl(url: str) -> str:
        with custom_span("olostep.scrape_url", {"url": url, "formats": ["markdown"]}):
            scrape = get_olostep_client().scrapes.create(url=url, formats=["markdown"])
            return convert_to_json_string(
                {"url": url, "scrape": {key: value for key, value in vars(scrape).items() if not key.startswith("_")}}, max_chars=10000
            )
        
    def _search_web_impl(query: str, limit: int = 8) -> str:
        with custom_span("olostep.search_web", {"query": query, "limit": limit}):
            search = get_olostep_client().searches.create(query=query, limit=limit)
            data = {key: value for key, value in vars(search).items() if not key.startswith("_")}
            return convert_to_json_string(
                {
                    "query": query,
                    "results": normalize_search_links(data.get("links", []), limit=limit),
                    "raw": data,
             }
            )


            
        