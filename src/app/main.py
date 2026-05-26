from app.config.logging import initialize_logger, get_logger
from app.config.settings import Settings
from app.research.assistant import ResearchAssistant
from app.model.research_models import MarkdownResearchReport
from app.agent.tools import build_tools
import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from app.research import send_email_with_attachment

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
    query:str = "Tell me about how AI is changing our life?"
    result: MarkdownResearchReport = await researchAgent.run_research(query)

    OUTPUT_DIR = Path("outputs")
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / "research_report.pdf"
    html = markdown.markdown(result.markdown_report)
    html_to_pdf(html, str(output_path))

    logger.info("Sending email with generated analysis...")
    send_email_with_attachment(query, output_path, settings)
    
    logger.info("Application shutdown...")

def html_to_pdf(html: str, output_path: str):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(output_path))
    story = [Paragraph(html, styles["Normal"])]
    doc.build(story)

if __name__ == "__main__":
    asyncio.run(main())