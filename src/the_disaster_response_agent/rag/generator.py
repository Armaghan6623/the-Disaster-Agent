import os
import json
from dotenv import load_dotenv
from groq import Groq
from the_disaster_response_agent.rag.retriever import retrieve
from the_disaster_response_agent.tools.weather_tool import get_weather
from the_disaster_response_agent.tools.resource_tool import find_nearby_resources

load_dotenv()
client = Groq(api_key=os.getenv("GROK_API"))

RAG_SYSTEM_PROMPT = """You are a disaster response assistant for NDMA Pakistan.
Use the provided protocol context to answer. If current weather conditions
would help assess the situation, use the get_weather tool. If the user
needs to know about nearby hospitals, shelters or relief resources, use
the find_nearby_resources tool. Always cite which protocol you're
referencing by title."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather conditions (temperature, precipitation, wind) for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number", "description": "Latitude of the location"},
                    "longitude": {"type": "number", "description": "Longitude of the location"},
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_nearby_resources",
            "description": "Find nearby hospitals, clinics, and emergency facilities near a given location using OpenStreetMap data",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number", "description": "Latitude of the incident location"},
                    "longitude": {"type": "number", "description": "Longitude of the incident location"},
                    "radius": {"type": "integer", "description": "Search radius in meters, default 5000"},
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
]

def generate_response(incident_text: str, top_k: int = 3) -> dict:
    retrieved_docs = retrieve(incident_text, top_k=top_k)
    context = "\n\n".join(f"[{doc['title']}]\n{doc['text']}" for doc in retrieved_docs)

    user_prompt = f"""Incident report: "{incident_text}"

Relevant protocols:
{context}

Based on the above, what is the recommended response action? Use available tools if they would help your assessment."""

    messages = [
        {"role": "system", "content": RAG_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    max_rounds = 4
    for _ in range(max_rounds):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            # No more tools needed — this is the final answer
            return {
                "incident": incident_text,
                "retrieved_docs": [d["title"] for d in retrieved_docs],
                "response": message.content,
            }

        # Model wants to call one or more tools — execute them
        messages.append(message)
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            fn_name = tool_call.function.name

            if fn_name == "get_weather":
                result = get_weather(**args)
            elif fn_name == "find_nearby_resources":
                result = find_nearby_resources(**args)
            else:
                result = {"error": f"Unknown tool {fn_name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

    return {
        "incident": incident_text,
        "retrieved_docs": [d["title"] for d in retrieved_docs],
        "response": "Max tool-call rounds reached without final answer.",
    }
