from the_disaster_response_agent.rag.embeddings import embed_text
from the_disaster_response_agent.utils.similarity import cosine_similarity

v1 = embed_text("Flood waters rising rapidly in residential area")
v2 = embed_text("Heavy flooding reported near homes")
v3 = embed_text("Earthquake damages several buildings downtown")

print("Flood vs Flood (should be high):", cosine_similarity(v1, v2))
print("Flood vs Earthquake (should be lower):", cosine_similarity(v1, v3))