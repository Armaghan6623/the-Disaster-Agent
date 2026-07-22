import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Measures how similar two embedding vectors are (0 to 1)."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def softmax(scores: np.ndarray) -> np.ndarray:
    """Converts raw model scores into probabilities that sum to 1."""
    exp_scores = np.exp(scores)
    return exp_scores / np.sum(exp_scores)