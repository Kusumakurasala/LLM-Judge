from typing import List
import numpy as np


def aggregate_results(results: List[dict]) -> dict:
    """
    Aggregate evaluation results across the test suite.
    """

    overall_scores = [r["overall_score"] for r in results]
    passed = [r["passed"] for r in results]

    return {
        "total_tests": len(results),
        "pass_rate": round(sum(passed) / len(results), 2) if results else 0,
        "average_score": round(float(np.mean(overall_scores)), 2) if overall_scores else 0,
        "max_score": round(float(np.max(overall_scores)), 2) if overall_scores else 0,
        "min_score": round(float(np.min(overall_scores)), 2) if overall_scores else 0,
    }