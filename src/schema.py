from pydantic import BaseModel, Field
from typing import List


class CriterionScore(BaseModel):
    name: str
    score: float = Field(ge=1, le=5)
    justification: str


class TestCase(BaseModel):
    question: str
    reference_answer: str
    candidate_answer: str


class PointwiseVerdict(BaseModel):
    scores: List[CriterionScore]
    overall_score: float
    passed: bool
    summary: str


class PairwiseTestCase(BaseModel):
    question: str
    answer_a: str
    answer_b: str


class PairwiseVerdict(BaseModel):
    winner: str
    reason: str


class SuiteReport(BaseModel):
    total_cases: int
    passed_cases: int
    failed_cases: int
    average_score: float