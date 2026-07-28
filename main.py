import json
from pathlib import Path

from src.aggregator import aggregate_results
from src.judge import LLMJudge
from src.logger import save_json_log
from src.mitigations import preprocess_test_case
from src.schema import TestCase
from src.validator import validate_verdict


DATA_FILE = Path("data/test_cases.json")
RESULTS_DIR = Path("results")


def load_test_cases():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return [TestCase(**item) for item in data]


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    judge = LLMJudge()

    verdicts = []

    test_cases = load_test_cases()

    print("=" * 60)
    print("LLM Judge Evaluation Started")
    print("=" * 60)

    for i, case in enumerate(test_cases, start=1):
        print(f"\nEvaluating Test Case {i}...")

        processed_case = preprocess_test_case(case)

        verdict = judge.evaluate(processed_case)

        if validate_verdict(verdict):
            verdicts.append(verdict)

            save_json_log(
                verdict,
                prefix=f"case_{i}"
            )

            print(f"✓ Score: {verdict.overall_score}")
        else:
            print("✗ Invalid verdict skipped.")

    report = aggregate_results(verdicts)

    report_path = RESULTS_DIR / "summary.json"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(
            report.model_dump(),
            f,
            indent=4
        )

    print("\n" + "=" * 60)
    print("Evaluation Complete")
    print("=" * 60)
    print(report)
    print(f"\nSummary saved to {report_path}")


if __name__ == "__main__":
    main()