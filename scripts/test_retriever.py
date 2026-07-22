from the_disaster_response_agent.rag.retriever import retrieve

results = retrieve("Water levels rising fast near residential homes, people trapped", top_k=3)

for r in results:
    print(f"[{r['score']:.3f}] {r['title']}")
    print(f"  {r['text'][:100]}...\n")