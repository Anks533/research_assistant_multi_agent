from app.config.logging import initialize_logger, get_logger
from app.config.settings import Settings
from app.research.assistant import ResearchAssistant
from app.model.research_models import MarkdownResearchReport
from app.agent.tools import build_tools

import asyncio

from dotenv import load_dotenv

async def main():

    load_dotenv()
    
    # 1️⃣ Load settings (fails fast if misconfigured)
    settings = Settings()

    # 2️⃣ Initialize logging
    initialize_logger(level=settings.log_level)
    logger = get_logger("main")

    logger.info("Application starting...")
    logger.info("Environment loaded successfully...")

    # 3️⃣ Run app
    tools = build_tools(settings)
    researchAgent = ResearchAssistant(tools)
    result: MarkdownResearchReport = await researchAgent.run_research("Tell me about how AI is changing our life?")
    with open("research_report.md", "w", encoding="utf-8") as f:
        f.write(result.markdown_report)

    logger.info("Application shutdown...")

if __name__ == "__main__":
    asyncio.run(main())