from openai import function_tool
from app.exception.exceptions import OlostepError
from agents import custom_span, Agent, Runner, RunResult
from app.config.settings import Settings
from app.helper.helper import get_olostep_client, convert_to_json_string, get_judge_agent
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
    async def search_with_scrape(self, query: str) -> list:
        """Search the web and scrape relevant sources."""
        ...

    @function_tool
    async def search_web(self, query: str) -> list:
        """Perform targeted web search."""
        ...

    @function_tool
    async def scrape_url(self, url: str) -> str:
        """Scrape a web page for content."""
        ...


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

            
        