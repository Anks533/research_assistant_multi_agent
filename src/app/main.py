from app.config.logging import initialize_logger, get_logger
from app.config.settings import Settings
from app.research.assistant import ResearchAssistant
from app.model.research_models import MarkdownResearchReport
from app.agent.tools import build_tools
import streamlit as st

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

    # Title of the application
    st.set_page_config(page_title="AI Research Assistant", layout="wide")
    st.title("📚 AI Research Assistant Multi-Agent System")
    question = st.text_area("Enter your research question:", height=120)
    start = st.button("🔍 Start Research")

    # 3️⃣ Run app
    if start and question:
        with st.spinner("Running multi-agent research..."):
            tools = build_tools(settings)
            researchAgent = ResearchAssistant(tools)
            result: MarkdownResearchReport = await researchAgent.run_research(question)
            st.success("Research completed")
            st.write(result.markdown_report)
            with open("research_report.md", "w", encoding="utf-8") as f:
                f.write(result.markdown_report)
            logger.info("Application shutdown...")

if __name__ == "__main__":
    asyncio.run(main())