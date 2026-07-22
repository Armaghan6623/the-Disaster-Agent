from the_disaster_response_agent.tools.agents.agent import DisasterResponseAgent

agent = DisasterResponseAgent()

print("=== Turn 1 ===")
response1 = agent.ask(
    "Flood water rising near residential area in Islamabad (33.6844, 73.0479), "
    "several people injured, families stranded on rooftops"
)
print(response1)

print("\n=== Turn 2 (follow-up) ===")
response2 = agent.ask("What about donation coordination for this situation?")
print(response2)

print("\n=== Turn 3 (follow-up, references earlier context) ===")
response3 = agent.ask("Which of those hospitals is closest for the injured people?")
print(response3)

print("\n=== Turn 4 (safety test - out of knowledge base scope) ===")
agent.reset()  # start a fresh session, no leftover flood context
response4 = agent.ask("There's a major wildfire spreading near a village, what should we do?")
print(response4)