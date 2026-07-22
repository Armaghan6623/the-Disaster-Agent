from the_disaster_response_agent.rag.generator import generate_response

result = generate_response(
    "Flood water rising near residential area in Islamabad (33.6844, 73.0479), "
    "several people injured, families stranded on rooftops"
)

print("Retrieved docs:", result["retrieved_docs"])
print("\nResponse:\n", result["response"])
