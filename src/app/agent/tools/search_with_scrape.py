from app.config.logging import get_logger
from agents import function_tool, custom_span, FunctionTool
from app.exception.exceptions import OlostepError
from app.helper.helper import get_olostep_client, convert_to_json_string, normalize_search_links
from app.config.settings import Settings

import logging
import asyncio

logger: logging.Logger = get_logger("search_with_scrape")

def build_search_with_scrape_tool(settings: Settings) -> FunctionTool:

    @function_tool
    async def search_with_scrape(query: str, limit: int = 5) -> list:
        """Search the web and scrape relevant sources."""
        try:
            logger.debug("Invoking search_with_scrape tool to call search API....")
            result = await asyncio.to_thread(_search_with_scrape_impl, query, settings, limit)
            logger.debug("Search API Completed....")
            logger.debug("Search Result :: \n")
            logger.debug(result)
        except Exception as exc:
            raise OlostepError(f"Olostep Search with Scrape failed: {exc}") from exc
        return result
    
    return search_with_scrape

def _search_with_scrape_impl(query: str, settings: Settings, limit: int = 5) -> str:

    scrape_options = {"formats":["markdown"], "timeout": 25}

    with custom_span("olostep.search_with_scrape", {"query": query, "limit": limit, "scrape_options": scrape_options}):
        search = get_olostep_client(settings).searches.create(
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