from agents import function_tool, Agent, custom_span, RunResult, Runner, FunctionTool
from app.helper.helper import get_judge_agent
from app.config.logging import get_logger
from app.model.research_models import Judgement

import logging

logger: logging.Logger = get_logger("judge_answer_quality")

def build_judge_answer_quality_tool() -> FunctionTool:

    @function_tool
    async def judge_answer_quality(query: str, evidence: str, stage: str = "current evidence") -> str:
        """Judge whether the current answer is sufficient."""
        logger.debug("Invoking judge_answer_quality tool...")
        prompt = f"""
        Original Research Query:
        {query}

        Evidence stage:
        {stage}

        Evidence to judge:
        {evidence}

        Return a structured judgement against this evidence of original query whether it is sufficient. 
        """

        logger.debug("Creating Judge Agent...")
        judge_agent: Agent = get_judge_agent()

        with custom_span("judge.answer.quality", {"stage": stage}):
            logger.debug("Starting Judge Agent...")
            result: RunResult = await Runner.run(judge_agent, prompt,max_turns=3)
            judgement: Judgement = result.final_output
            judgement_json = judgement.model_dump_json()
            logger.debug("Judge Agent completed...")
            logger.debug("Judgement :: \n")
            logger.debug(judgement_json)
        return judgement_json
    
    return judge_answer_quality