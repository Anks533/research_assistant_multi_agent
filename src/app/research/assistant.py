import logging

from app.config.logging import get_logger
from agents import gen_trace_id, trace, custom_span, Runner, flush_traces, RunResult
from app.model.research_models import MarkdownResearchReport
from app.exception.exceptions import MultiAgentResearchException
from app.helper.helper import get_manager_agent

logger:logging.Logger = get_logger("ResearchAssistant")


class ResearchAssistant:

    def __init__(self, tools: list) -> None:
        self.tools = tools

    async def run_research(self, query: str) -> MarkdownResearchReport :
        """ Perform research on the given user query """
        try:
            trace_id = gen_trace_id()
            logger.debug("Trace ID for the request: %s", trace_id)
            logger.debug("Trace URI for the request: %s", f"https://platform.openai.com/logs/trace?trace_id={trace_id}")
            prompt = f"""
                Research question:
                {query}

                Return a polished, reader-friendly Markdown research report with substantial detail for the user's specific question. Follow the required workflow exactly:
                - Use answer_query first for a simple initial answer.
                - Use the judge agent immediately after the simple answer to decide whether to stop or continue.
                - If the first judge says the answer is not sufficient, run search_with_scrape.
                - Use the judge agent immediately after search_with_scrape to decide whether to stop or continue.
                - If the second judge still says the evidence is weak, do not judge again. Run multiple targeted search_web calls, choose at least the top 3 relevant source URLs from the search results, and scrape those top 3 pages for context.
                - Analyst agent writes the final Markdown report from all answer, judge, search, and scrape evidence. Do not include Limitations or Next Steps sections.
            """
            result = await self._run_workflow(query, trace_id, prompt)
            return result.final_output
        except Exception as ex:
            logger.error(f"Exception occured while running the research : {ex}")
            raise MultiAgentResearchException(f"Exception occured while running the research : {ex}") from ex

    async def _run_workflow(self, query, trace_id, prompt) -> RunResult:
        logger.debug("Starting Research Workflow....")
        with trace(
            workflow_name="research_assistant_using_multi_agent_system",
            trace_id=trace_id,
            metadata={
                "query": query,
                "application": "research_assistant"
            }
        ):
            with custom_span(
                name="manager.run",
                data={
                    "query": query
                }
            ):
                result = await Runner.run(
                    starting_agent=get_manager_agent(self.tools),
                    input=prompt,
                    max_turns=20
                )
        flush_traces()
        logger.debug("Completed Research Workflow....")
        return result
    





