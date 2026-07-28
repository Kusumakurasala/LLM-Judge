import json
import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential

from src.schema import CriterionScore, PointwiseVerdict, TestCase


load_dotenv()


class LLMJudge:
    def __init__(
        self,
        rubric_path: str = "config/rubric.yaml",
        suite_config_path: str = "config/suite_config.yaml",
    ) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to the .env file."
            )

        self.client = genai.Client(api_key=api_key)
        self.rubric = self._load_yaml(rubric_path)
        self.config = self._load_yaml(suite_config_path)

        self.model = self.config.get(
            "judge_model",
            "gemini-2.0-flash",
        )

    @staticmethod
    def _load_yaml(file_path: str) -> dict[str, Any]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return data or {}

    def _build_prompt(self, test_case: TestCase) -> str:
        criteria = self.rubric.get("criteria", {})

        rubric_lines = []

        for name, details in criteria.items():
            description = details.get("description", "")
            weight = details.get("weight", 1.0)

            rubric_lines.append(
                f"- {name}: {description} Weight: {weight}"
            )

        rubric_text = "\n".join(rubric_lines)

        return f"""
You are an impartial LLM evaluator.

Evaluate the candidate answer using the rubric below.

Question:
{test_case.question}

Reference answer:
{test_case.reference_answer}

Candidate answer:
{test_case.candidate_answer}

Rubric:
{rubric_text}

Scoring scale:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

Return only valid JSON using this structure:

{{
  "scores": [
    {{
      "name": "correctness",
      "score": 1,
      "justification": "Explanation"
    }}
  ],
  "overall_score": 1.0,
  "passed": false,
  "summary": "Overall explanation"
}}

Include one score entry for every rubric criterion.
Do not include Markdown code fences.
"""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True,
    )
    def evaluate(self, test_case: TestCase) -> PointwiseVerdict:
        prompt = self._build_prompt(test_case)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise ValueError("The judge model returned an empty response.")

        raw_result = response.text.strip()

        if raw_result.startswith("```"):
            raw_result = raw_result.replace("```json", "")
            raw_result = raw_result.replace("```", "")
            raw_result = raw_result.strip()

        result = json.loads(raw_result)

        scores = [
            CriterionScore(**score)
            for score in result["scores"]
        ]

        pass_score = float(
            self.config.get("pass_score", 3.5)
        )

        overall_score = float(result["overall_score"])

        return PointwiseVerdict(
            scores=scores,
            overall_score=overall_score,
            passed=overall_score >= pass_score,
            summary=result["summary"],
        )