from typing import Dict


def evaluate_pairwise_unbiased(judge_client, test_case, response_a, response_b) -> Dict:
    """
    Evaluate A vs B and B vs A to reduce position bias.
    """

    # First evaluation: A vs B
    forward = judge_client.judge_pair(
        input_text=test_case["input"],
        output_a=response_a,
        output_b=response_b,
    )

    # Second evaluation: B vs A
    reverse = judge_client.judge_pair(
        input_text=test_case["input"],
        output_a=response_b,
        output_b=response_a,
    )

    # Map the reversed result back to the original labels
    reverse_winner = {
        "Model_A": "Model_B",
        "Model_B": "Model_A",
        "Tie": "Tie",
    }.get(reverse.winner, "Tie")

    consistent = (forward.winner == reverse_winner)

    final_winner = (
        forward.winner
        if consistent
        else "Tie (Position Inconsistency)"
    )

    return {
        "forward_winner": forward.winner,
        "reverse_winner": reverse_winner,
        "position_consistent": consistent,
        "final_winner": final_winner,
    }