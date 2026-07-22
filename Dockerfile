FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

# Step 1: install ONLY dependencies (not your own package yet) — this layer
# gets cached and skipped on rebuilds unless pyproject.toml/uv.lock change
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Step 2: now copy actual source code
COPY . .

# Step 3: install your own project now that src/ actually exists
RUN uv sync --frozen --no-dev

RUN mkdir -p logs

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "the_disaster_response_agent.api.main:app", "--host", "0.0.0.0", "--port", "8000"]