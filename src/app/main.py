from app.config.logging import initialize_logger, get_logger
from app.config.settings import Settings
from app.research.assistant import ResearchAssistant

def main():
    # 1️⃣ Load settings (fails fast if misconfigured)
    settings = Settings()

    # 2️⃣ Initialize logging
    initialize_logger(level=settings.log_level)
    logger = get_logger("main")

    logger.info("Application starting...")
    logger.info("Environment loaded successfully...")

    # 3️⃣ Run app
    researchAgent = ResearchAssistant(settings)
    researchAgent.run_research("Tell me about how AI is changing our life?")

    logger.info("Application shutdown...")

if __name__ == "__main__":
    main()