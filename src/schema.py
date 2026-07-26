from pydantic import BaseModel
from typing import Dict


class CriterionScore(BaseModel):
    score: int
    rationale: str


class EvaluationResult(BaseModel):
    criteria_breakdown: Dict[str, CriterionScore]
    overall_score: float
    overall_rationale: str
    passed: bool