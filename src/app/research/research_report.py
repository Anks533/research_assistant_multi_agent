from pydantic import BaseModel, Field


class ResearchReport(BaseModel):
    markdown_report: str
