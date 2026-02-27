# Python MCP UI Server - Docker image with uv
# Run: stdio → python server.py | HTTP → python server.py --http --port 3000
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies (no dev group); omit --frozen if uv.lock is missing
RUN uv sync --no-dev --no-install-project

# Copy application
COPY server.py ./

# Expose HTTP port (default 3000)
EXPOSE 3000

# Run the MCP server with HTTP (SSE) transport; matches: python server.py --http --port 3000
CMD ["uv", "run", "python3", "server.py", "--http", "--port", "3000"]
