from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, good quality

def embed_text(text: str) -> np.ndarray:
    """Converts a string into a dense vector embedding."""
    return _model.encode(text, convert_to_numpy=True)

def embed_batch(texts: list[str]) -> np.ndarray:
    """Converts a list of strings into embeddings (more efficient than one-by-one)."""
    return _model.encode(texts, convert_to_numpy=True)