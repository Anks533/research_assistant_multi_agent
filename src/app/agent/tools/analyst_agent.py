from agents import FunctionTool
from app.helper.helper import get_analyst_agent

def build_analyst_agent_tool() -> FunctionTool:
    return get_analyst_agent().as_tool(
                    tool_name="write_markdown_research_report",
                    tool_description="Write the final structured Markdown research report from the gathered evidence.",
                )