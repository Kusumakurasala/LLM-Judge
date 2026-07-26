from sklearn.metrics import cohen_kappa_score
import numpy as np


def calculate_judge_accuracy_and_kappa(human_scores, judge_scores):
    """
    Compare judge scores with human scores.
    Returns exact agreement and Cohen's Kappa.
    """

    human = np.array(human_scores)
    judge = np.array(judge_scores)

    exact_agreement = np.mean(human == judge)

    kappa = cohen_kappa_score(
        human,
        judge,
        weights="quadratic"
    )

    return {
        "sample_size": len(human),
        "exact_agreement_rate": float(exact_agreement),
        "cohens_kappa": float(kappa)
    }