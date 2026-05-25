from openai import function_tool
from app.exception.exceptions import OlostepError
from agents import custom_span
from app.config.settings import Settings
from app.helper.helper import get_olostep_client, convert_to_json_string, get_judge_agent
from olostep.models.response import AnswersResponse


import asyncio

class Toolset:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @function_tool
    async def answer_query(self, query: str) -> str:
        """Provide a simple initial answer without deep research using Olostep Answer API."""
        try:
            result = await asyncio.to_thread(self._answer_query_impl, query)
        except Exception as ex:
            raise OlostepError(f"Olostep Answer API failed with exception : {ex}") from ex
        return result

    @function_tool
    async def judge_answer_quality(self, query: str, evidence: str) -> str:
        """Judge whether the current answer is sufficient."""
        prompt = f"""
        Original Research Query:
        {query}

        Evidence to judge:
        {evidence}

        Return a structured judgement against this evidence of original query whether it is sufficient. 
        """

        get_judge_agent



        

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

            
        