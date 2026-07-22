# Disaster Response Agent

AI-powered disaster response assessment system using transformers.

## Installation

```bash
pip install -e .
```

## Usage

```python
from the_disaster_response_agent.agent import DisasterResponseAgent

agent = DisasterResponseAgent()
result = agent.assess_incident("Flood reported in downtown area")
print(result)
```

## Development

```bash
uv sync
uv run ruff check .
uv run python scripts/verify.py
```