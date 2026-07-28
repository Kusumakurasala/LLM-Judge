from typing import List

from src.schema import PointwiseVerdict, SuiteReport


def aggregate_results(verdicts: List[PointwiseVerdict]) -> SuiteReport:
    """
    Aggregate multiple evaluation results into a summary report.
    """

    if not verdicts:
        return SuiteReport(
            total_cases=0,
            passed_cases=0,
            failed_cases=0,
            average_score=0.0,
        )

    total_cases = len(verdicts)
    passed_cases = sum(1 for v in verdicts if v.passed)
    failed_cases = total_cases - passed_cases

    average_score = sum(v.overall_score for v in verdicts) / total_cases

    return SuiteReport(
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=failed_cases,
        average_score=round(average_score, 2),
    )