import json
from pathlib import Path

from src.judge import LLMJudge
from src.aggregator import aggregate_results
from src.report import generate_html_report


def main():
    judge = LLMJudge()

    input_file = Path("data/test_suites/general_qa.json")
    output_file = Path("results/evaluation_results.json")

    with open(input_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []

    for test in test_cases:

        prompt = f"""
Question:
{test["input"]}

Expected Answer:
{test["expected"]}

Evaluate the expected answer.

Return ONLY valid JSON.
"""

        verdict = judge.evaluate(prompt)

        result = verdict.model_dump()

        result["id"] = test["id"]
        result["question"] = test["input"]

        results.append(result)

    summary = aggregate_results(results)

    # Generate HTML report
    generate_html_report(summary, results)

    output = {
        "summary": summary,
        "results": results
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("\nEvaluation completed.")
    print(f"Results saved to {output_file}")
    print("HTML report generated: results/report.html")


if __name__ == "__main__":
    main()