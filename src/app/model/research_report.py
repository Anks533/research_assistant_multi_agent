from pydantic import BaseModel

class ResearchReport(BaseModel):
    markdown_report: str
