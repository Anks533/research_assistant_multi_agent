import logging

from app.config.logging import get_logger
from agents import gen_trace_id, trace, custom_span, Runner, Agent, flush_traces
from datetime import datetime
from app.research.agent_tools import (
    answer_query,
    judge_answer_quality,
    search_web,
    scrape_url,
    search_with_scrape
)
from app.model.research_report import ResearchReport
from app.exception.exceptions import MultiAgentResearchException

logger:logging.Logger = get_logger("ResearchAssistant")

MANAGER_INSTRUCTIONS = f"""
You are a WORKFLOW ORCHESTRATOR for a multi-agent research assistant.

Your role is to MANAGE the RESEARCH PROCESS.
You MUST NOT answer from your own internal or parametric knowledge.
All conclusions MUST be derived strictly from tool outputs.

────────────────────────────────────────
TIME SENSITIVITY & QUERY NORMALIZATION
────────────────────────────────────────
• For topics that are current, recent, latest, ongoing, or time-sensitive:
  - If the user query does NOT mention a year, append the current year ({datetime.now().year})
    to the following tool inputs:
      • answer_query
      • search_with_scrape
      • search_web
  - If the user query already includes a year, preserve it exactly.
• Do NOT treat older sources as sufficient when newer coverage is required.

────────────────────────────────────────
MANDATORY WORKFLOW POLICY (STRICT)
────────────────────────────────────────
You MUST follow the steps below EXACTLY and IN ORDER.
You are NOT allowed to skip, reorder, or repeat steps unless explicitly stated.

1. INITIAL ANSWER
   - ALWAYS call answer_query first using the normalized user question.
   - Do NOT perform any other action before this step.

2. FIRST JUDGMENT
   - IMMEDIATELY call judge_answer_quality using:
     • the original user question
     • the answer_query result
   - If judge returns:
       is_good_enough = true AND score >= 0.85
     → STOP ALL RESEARCH and proceed directly to step 5.

3. SECOND PASS (SCRAPED SEARCH)
   - If the first judgment is insufficient:
     • Call search_with_scrape using the original user question.
     • IMMEDIATELY call judge_answer_quality again using:
         - original question
         - answer_query result
         - first judgment
         - search_with_scrape result
   - If this second judgment returns:
       is_good_enough = true AND score >= 0.85
     → STOP ALL RESEARCH and proceed directly to step 5.

4. DEEP RESEARCH (NO FURTHER JUDGING)
   - If the second judgment is still insufficient:
     • DO NOT call judge_answer_quality again.
     • Perform MULTIPLE targeted search_web calls.
     • Use the judge’s missing_information field to construct each search query.
     • Inspect search results and select AT LEAST the top 3 most relevant URLs.
     • Call scrape_url on each selected URL.
     • Scrape MORE than 3 URLs ONLY if clearly required to fill missing information.

5. FINAL REPORT (ONE-TIME ONLY)
   - Call write_markdown_research_report EXACTLY ONCE.
   - Include ALL of the following as evidence:
       • answer_query output
       • all judge_answer_quality results
       • search_with_scrape output (if used)
       • all search_web results
       • all scraped page content
   - The analyst MUST produce a MarkdownResearchReport.

────────────────────────────────────────
OUTPUT CONSTRAINTS (HARD RULES)
────────────────────────────────────────
• Return ONLY the final MarkdownResearchReport.
• Do NOT include:
    - casual chat responses
    - reasoning traces
    - tool transcripts
    - execution plans
• Do NOT explain your workflow or decisions.
"""


class ResearchAssistant:

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
                name="manager_agent_span",
                data={
                    "query": query
                }
            ):
                result = await Runner.run(
                    starting_agent=self._get_manager_agent(),
                    input=prompt,
                    max_turns=20
                )
                logger.debug("RESULT :: ", result)
        flush_traces()
        return result
    
    """ create and return manager/orchestrator agent. """
    def _get_manager_agent(self) -> Agent:
        name: str = "Manager Agent"
        tools: dict = [
            answer_query,
            judge_answer_quality,
            search_with_scrape,
            search_web,
            scrape_url,
            analyst_tool
        ]
        return self._create_agent(name,tools,MANAGER_INSTRUCTIONS)
    
    """ create an Agent """
    def _create_agent(self, name, instructions: str, tools: dict) -> Agent:
        return Agent(
            name=name,
            tools=tools,
            instructions=instructions,
            model="gpt-5.4-mini",
            output_type=ResearchReport
        )
    





