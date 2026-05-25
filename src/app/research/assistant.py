import logging

from app.config.logging import get_logger
from app.config.settings import Settings
from agents import gen_trace_id, trace, custom_span, Runner, flush_traces
from app.model.research_models import ResearchReport
from app.exception.exceptions import MultiAgentResearchException
from app.research.agent_tools import Toolset
from app.helper.helper import get_manager_agent, get_analyst_agent

logger:logging.Logger = get_logger("ResearchAssistant")


class ResearchAssistant:

    def __init__(self, settings:Settings) -> None:
        self.settings = settings

    async def run_research(self, query: str) -> ResearchReport :
        """ Perform research on the given user query """
        try:
            trace_id = gen_trace_id()
            logger.debug("Trace ID for the request: ", trace_id)
            logger.debug("Trace URI for the request: ", f"https://platform.openai.com/logs/trace?trace_id={trace_id}")
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
            logger.error("Exception occured while running the research : {ex}")
            raise MultiAgentResearchException("Exception occured while running the research : {ex}") from ex

    async def _run_workflow(self, query, trace_id, prompt):
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
                analyst_tool = get_analyst_agent().as_tool(
                    tool_name="write_markdown_research_report",
                    tool_description="Write the final structured Markdown research report from the gathered evidence.",
                )

                tool_set = Toolset(self.settings)
                tools:dict = [
                    tool_set.answer_query,
                    tool_set.judge_answer_quality,
                    tool_set.search_with_scrape,
                    tool_set.search_web,
                    tool_set.scrape_url,
                    analyst_tool,
                ]
                result = await Runner.run(
                    starting_agent=get_manager_agent(tools),
                    input=prompt,
                    max_turns=20
                )
                logger.debug("RESULT :: ", result) ## TODO::
        flush_traces()
        return result
    





