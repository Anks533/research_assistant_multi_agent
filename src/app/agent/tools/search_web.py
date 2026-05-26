from agents import function_tool, custom_span, FunctionTool
from app.exception.exceptions import OlostepError
from app.config.settings import Settings
from app.helper.helper import get_olostep_client, convert_to_json_string, normalize_search_links

import asyncio

def build_search_web_tool(settings: Settings) -> FunctionTool:

    @function_tool
    async def search_web(query: str, limit: int = 8) -> list:
        """Search the web using Olostep Search and return normalized results."""
        try:
            result = await asyncio.to_thread(_search_web_impl, query, settings, limit)
        except Exception as exc:
            raise OlostepError(f"Olostep Search API failed: {exc}") from exc
        return result
    
    return search_web

def _search_web_impl(query: str, settings: Settings, limit: int = 8) -> str:
    with custom_span("olostep.search_web", {"query": query, "limit": limit}):
        search = get_olostep_client(settings).searches.create(query=query, limit=limit)
        data = {key: value for key, value in vars(search).items() if not key.startswith("_")}
        return convert_to_json_string(
            {
                "query": query,
                "results": normalize_search_links(data.get("links", []), limit=limit),
                "raw": data,
            }
        )