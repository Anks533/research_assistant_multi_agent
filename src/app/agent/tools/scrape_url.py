from agents import function_tool, custom_span, FunctionTool
from app.exception.exceptions import OlostepError
from app.config.settings import Settings
from app.helper.helper import get_olostep_client, convert_to_json_string

import asyncio

def build_scrape_url_tool(settings: Settings) -> FunctionTool:

    @function_tool
    async def scrape_url(url: str) -> str:
        """Scrape one URL with Olostep and return compact page content."""
        try:
            result = await asyncio.to_thread(_scrape_url_impl, url, settings)
        except Exception as exc:
            raise OlostepError(f"Olostep Scrape API failed: {exc}") from exc
        return result
    
    return scrape_url

def _scrape_url_impl(url: str, settings: Settings) -> str:
    with custom_span("olostep.scrape_url", {"url": url, "formats": ["markdown"]}):
        scrape = get_olostep_client(settings).scrapes.create(url=url, formats=["markdown"])
        return convert_to_json_string(
            {
                "url": url, 
                "scrape": {
                    key: value for key, value in vars(scrape).items() if not key.startswith("_")
                }
            }, 
            max_chars=10000
        )