import numpy as np
from the_disaster_response_agent.utils.similarity import cosine_similarity, softmax

def test_cosine_similarity_identical_vectors():
    v = np.array([0.9, 0.1, 0.2])
    assert abs(cosine_similarity(v, v) - 1.0) < 1e-6


def test_cosine_similarity_dissimilar_vectors():
    flood = np.array([0.9, 0.1, 0.2])
    earthquake = np.array([0.1, 0.9, 0.8])
    sim = cosine_similarity(flood, earthquake)
    assert sim < 0.5


def test_softmax_sums_to_one():
    scores = np.array([2.1, 0.5, 3.2])
    probs = softmax(scores)
    assert abs(np.sum(probs) - 1.0) < 1e-6
