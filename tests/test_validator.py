from src.schema import CriterionScore, PointwiseVerdict
from src.validator import validate_verdict


def test_valid_verdict():
    verdict = PointwiseVerdict(
        scores=[
            CriterionScore(
                name="correctness",
                score=5,
                justification="Correct"
            )
        ],
        overall_score=5,
        passed=True,
        summary="Excellent"
    )

    assert validate_verdict(verdict) is True


def test_invalid_overall_score():
    verdict = PointwiseVerdict(
        scores=[
            CriterionScore(
                name="correctness",
                score=5,
                justification="Correct"
            )
        ],
        overall_score=6,
        passed=True,
        summary="Invalid"
    )

    assert validate_verdict(verdict) is False