from src.schema import PointwiseVerdict


def validate_verdict(verdict: PointwiseVerdict) -> bool:
    """
    Validate a PointwiseVerdict object.
    """

    if not verdict.scores:
        return False

    if not (1 <= verdict.overall_score <= 5):
        return False

    for score in verdict.scores:
        if not (1 <= score.score <= 5):
            return False

    return True