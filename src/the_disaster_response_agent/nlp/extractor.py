import json
import os
from dotenv import load_dotenv
from groq import Groq
from the_disaster_response_agent.data.schema import DisasterEvent
from the_disaster_response_agent.nlp.prompts import EXTRACTION_SYSTEM_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROK_API"))

def extract_from_text(text: str, source: str = "unknown") -> DisasterEvent:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=300,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": f'Text: "{text}"'},
        ],
    )

    raw = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {}

    return DisasterEvent(
        text=text,
        source=source,
        disaster_type=parsed.get("disaster_type"),
        humanitarian_category=parsed.get("humanitarian_category"),
        severity=parsed.get("severity"),
        location=parsed.get("location"),
        raw_metadata=parsed,
    )