from pydantic import BaseModel, Field

class ResearchReport(BaseModel):
    markdown_report: str

class Judgement(BaseModel):
    is_good_enough: bool = Field(description="Whether evidence fully addresses the question with strong, specific, and relevant source support")
    score: float = Field(ge=0, le=1, description="Evidence queality score between 0 and 1")
    descision_reason: str = Field(description="Short explanation of the descision taken.")
    missing_info: list[str] = Field(
        default_factory=list,
        description="List all important gaps that need to be fixed."
    )

