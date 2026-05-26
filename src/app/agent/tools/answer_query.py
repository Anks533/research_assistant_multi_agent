from agents import function_tool, FunctionTool

from app.config.logging import get_logger
from app.exception.exceptions import OlostepError
from app.config.settings import Settings
from app.helper.helper import get_olostep_client, convert_to_json_string
from olostep.models.response import AnswersResponse
from agents import custom_span

import logging
import asyncio

logger: logging.Logger = get_logger("answer_query")

def build_answer_query_tool(settings: Settings) -> FunctionTool:

    @function_tool
    async def answer_query(query: str) -> str:
        """Provide a simple initial answer without deep research using Olostep Answer API."""
        try:
            logger.debug("Invoking answer_query tool to call Answer API...")
            result = await asyncio.to_thread(_answer_query_impl, query, settings)
            logger.debug("Olostep Answer API Response :: \n")
            logger.debug(result)
        except Exception as ex:
            raise OlostepError(f"Olostep Answer API failed with exception : {ex}") from ex
        return result
    return answer_query


""" call Answer api and return json string response. """
def _answer_query_impl(query: str, settings: Settings) -> str:
    with custom_span(
        name = "olostep.answer_query",
        data = {
            "query": query
        }
    ):
        result: AnswersResponse = get_olostep_client(settings).answers.create(task=query)
        result_dict: dict = vars(result)
        return convert_to_json_string(result_dict)