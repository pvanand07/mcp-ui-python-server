# Python MCP UI Server - Docker image with uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies (no dev group); omit --frozen if uv.lock is missing
RUN uv sync --no-dev --no-install-project

# Copy application
COPY server.py ./

# Expose HTTP port
EXPOSE 3000

# Run the MCP server with HTTP SSE transport
CMD ["uv", "run", "python", "server.py", "--http", "--port", "3000"]
