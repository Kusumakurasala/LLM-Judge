import os
import json

from google import genai

from src.schema import EvaluationResult

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class LLMJudge:

    def __init__(self):
        self.model = "models/gemini-3.6-flash"

    def evaluate(self, prompt: str) -> EvaluationResult:

        system_prompt = f"""
You are an expert LLM evaluator.

Evaluate the answer using these criteria:

1. Correctness
2. Relevance
3. Completeness
4. Clarity

Each criterion must have

- score (1-5)
- rationale

Return ONLY valid JSON matching exactly this format:

{{
  "criteria_breakdown": {{
      "correctness": {{
          "score":5,
          "rationale":"..."
      }},
      "relevance": {{
          "score":5,
          "rationale":"..."
      }},
      "completeness": {{
          "score":5,
          "rationale":"..."
      }},
      "clarity": {{
          "score":5,
          "rationale":"..."
      }}
  }},
  "overall_score":5,
  "overall_rationale":"...",
  "passed":true
}}

Question:

{prompt}
"""

        response = client.models.generate_content(
            model=self.model,
            contents=system_prompt,
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        data = json.loads(text)

        return EvaluationResult.model_validate(data)