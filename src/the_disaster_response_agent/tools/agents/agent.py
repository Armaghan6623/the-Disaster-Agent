import os
import json
import time
from dotenv import load_dotenv
from groq import Groq, BadRequestError
from the_disaster_response_agent.rag.retriever import retrieve
from the_disaster_response_agent.tools.weather_tool import get_weather
from the_disaster_response_agent.tools.resource_tool import find_nearby_resources

load_dotenv()

SYSTEM_PROMPT = """You are a disaster response assistant for NDMA Pakistan.
Use the provided protocol context and available tools to answer questions.
Always cite which protocol you're referencing by title when giving disaster
response guidance.

CRITICAL RULE — only applies to disaster-type/hazard mismatches:
If the user's question is about a disaster type (e.g. wildfire, landslide)
that none of your retrieved protocols actually cover, do NOT apply a protocol
written for a different disaster type (e.g. earthquake) to it. Instead say
clearly that you lack validated protocol guidance for that specific hazard,
and that a human responder with relevant expertise should be consulted.

This rule does NOT apply to simple factual, geographic, or data-lookup
questions (e.g. "which hospital is closest", "what's the weather") — for
those, just answer directly using the tool data available, no disclaimer
needed.

If current weather or nearby resources would help your assessment, use the
available tools. Maintain awareness of the ongoing incident across the
conversation."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather conditions (temperature, precipitation, wind) for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_nearby_resources",
            "description": "Find nearby hospitals, clinics, and emergency facilities near a location using OpenStreetMap",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                    "radius": {"type": "integer", "description": "Search radius in meters, default 5000"},
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "find_nearby_resources": find_nearby_resources,
}


class DisasterResponseAgent:
    """A stateful agent that maintains conversation history across turns."""

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROK_API"))
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def ask(self, user_input: str, top_k: int = 3, max_rounds: int = 4) -> str:
        """Send a new message (initial incident or follow-up) and get a response."""

        # Ground the new input with fresh RAG retrieval every turn
        retrieved_docs = retrieve(user_input, top_k=top_k)
        context = "\n\n".join(f"[{doc['title']}]\n{doc['text']}" for doc in retrieved_docs)

        augmented_input = f"""{user_input}

Relevant protocols for this message:
{context}"""

        self.messages.append({"role": "user", "content": augmented_input})

        for round_num in range(max_rounds):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=500,
                    messages=self.messages,
                    tools=TOOLS,
                    temperature=0.3,
                )
            except BadRequestError as e:
                if "tool_use_failed" in str(e) and round_num < max_rounds - 1:
                    print(f"[Retry] Tool call generation failed, retrying (round {round_num + 1})...")
                    time.sleep(1)
                    continue
                else:
                    self.messages.append({
                        "role": "assistant",
                        "content": "I encountered an issue calling tools. Here's my assessment based on available protocol context only."
                    })
                    return self.messages[-1]["content"]

            message = response.choices[0].message

            if not message.tool_calls:
                self.messages.append({"role": "assistant", "content": message.content})
                return message.content

            self.messages.append(message)
            for tool_call in message.tool_calls:
                args = json.loads(tool_call.function.arguments)
                fn_name = tool_call.function.name
                fn = TOOL_FUNCTIONS.get(fn_name)
                result = fn(**args) if fn else {"error": f"Unknown tool {fn_name}"}

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })

        return "Max tool-call rounds reached without a final answer."

    def reset(self):
        """Clear conversation history, start a new incident session."""
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
