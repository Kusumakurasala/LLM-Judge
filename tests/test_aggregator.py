from src.schema import PointwiseVerdict
from src.aggregator import aggregate_results


def test_aggregate_results():
    verdict1 = PointwiseVerdict(
        scores=[],
        overall_score=5,
        passed=True,
        summary="Good"
    )

    verdict2 = PointwiseVerdict(
        scores=[],
        overall_score=3,
        passed=False,
        summary="Average"
    )

    report = aggregate_results([verdict1, verdict2])

    assert report.total_cases == 2
    assert report.passed_cases == 1
    assert report.failed_cases == 1
    assert report.average_score == 4.0