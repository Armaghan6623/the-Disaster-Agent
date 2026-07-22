from the_disaster_response_agent.rag.know_base import KNOWLEDGE_BASE
from the_disaster_response_agent.rag.embeddings import embed_text, embed_batch
from the_disaster_response_agent.utils.similarity import cosine_similarity

# Precompute embeddings for the knowledge base once, at import time
_kb_texts = [doc["text"] for doc in KNOWLEDGE_BASE]
_kb_embeddings = embed_batch(_kb_texts)

def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Given a query (e.g. incident text), return the top_k most relevant
    documents from the knowledge base, ranked by cosine similarity.
    """
    query_vec = embed_text(query)

    scored = []
    for doc, doc_vec in zip(KNOWLEDGE_BASE, _kb_embeddings):
        score = cosine_similarity(query_vec, doc_vec)
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"score": float(score), **doc} for score, doc in scored[:top_k]]