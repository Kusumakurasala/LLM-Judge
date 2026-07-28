import json
from src.schema import PointwiseVerdict, CriterionScore


def parse_judge_response(response_text: str) -> PointwiseVerdict:
    """
    Parse the JSON response returned by the LLM Judge.
    """

    data = json.loads(response_text)

    scores = [
        CriterionScore(**score)
        for score in data["scores"]
    ]

    return PointwiseVerdict(
        scores=scores,
        overall_score=data["overall_score"],
        passed=data["passed"],
        summary=data["summary"],
    )