import random

from src.schema import TestCase


def shuffle_answers(test_case: TestCase) -> TestCase:
    """
    Shuffle answer order to reduce position bias.
    """
    answers = [
        test_case.reference_answer,
        test_case.candidate_answer,
    ]

    random.shuffle(answers)

    return TestCase(
        question=test_case.question,
        reference_answer=answers[0],
        candidate_answer=answers[1],
    )


def normalize_text(text: str) -> str:
    """
    Normalize whitespace to reduce formatting/style bias.
    """
    return " ".join(text.split())


def truncate_answer(text: str, max_words: int = 200) -> str:
    """
    Reduce verbosity bias by limiting answer length.
    """
    words = text.split()

    if len(words) <= max_words:
        return text

    return " ".join(words[:max_words])


def preprocess_test_case(test_case: TestCase) -> TestCase:
    """
    Apply all mitigation steps before evaluation.
    """
    return TestCase(
        question=normalize_text(test_case.question),
        reference_answer=truncate_answer(
            normalize_text(test_case.reference_answer)
        ),
        candidate_answer=truncate_answer(
            normalize_text(test_case.candidate_answer)
        ),
    )