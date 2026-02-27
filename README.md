# Python MCP UI Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that returns **MCP-UI** resources so hosts can render interactive UIs for tools. Built with [FastMCP](https://github.com/jlowin/fastmcp) and [mcp-ui-server](https://pypi.org/project/mcp-ui-server/).

## What's included

- **greet** – Simple HTML greeting widget
- **show_dashboard** – Sample dashboard with metric cards
- **show_external_site** – External URL in an iframe (example.com)
- **show_interactive_demo** – Buttons that send intents and tool calls via `postMessage`

## Setup

**Using uv (recommended):**

```powershell
uv sync
```

**Using pip:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install mcp mcp-ui-server
```

## Run

**Stdio (for CLI / IDE MCP clients):**

```powershell
uv run python server.py
# or: python server.py
```

**HTTP with SSE (for web clients, e.g. ui-inspector):**

```powershell
uv run python server.py --http --port 3000
```

Then connect at `http://localhost:3000/sse` with transport type **SSE**.

**Using Docker:**

```powershell
docker compose up --build
```

The server runs with `uv run python server.py --http --port 3000` and is available at `http://localhost:3000/sse`.

## Use in Cursor (over URL)

1. **Start the server with HTTP/SSE** (in a terminal, keep it running):

   ```powershell
   uv run python server.py --http --port 3000
   ```

2. This project’s `.cursor/mcp.json` is set to use **URL** (`http://localhost:3000/sse`). Restart Cursor so it picks up the config.

3. The server must be running before you use MCP in Cursor. To run it automatically when opening the project, start the command above in a separate terminal or run it as a background process.

## Use in Claude Desktop

Claude Desktop talks to MCP servers over **stdio** by default. Using a **URL** (e.g. via ngrok) is only supported in some setups and can trigger “check your server URL and make sure your server handles auth correctly” if the client gets an HTML interstitial or wrong endpoint.

### Option 1: Stdio (recommended, no ngrok)

1. Open your Claude Desktop config. On Windows it is usually:
   - `%APPDATA%\Claude\claude_desktop_config.json`
2. Add this server (replace the path with your real project path):

```json
{
  "mcpServers": {
    "mcp-ui-python": {
      "command": "uv",
      "args": ["run", "python", "I:\\DEV\\MCP-UI\\server.py"]
    }
  }
}
```

If you don’t use `uv`, use your venv’s Python:

```json
"mcp-ui-python": {
  "command": "I:\\DEV\\MCP-UI\\.venv\\Scripts\\python.exe",
  "args": ["I:\\DEV\\MCP-UI\\server.py"]
}
```

3. Restart Claude Desktop. The server runs when Claude starts; no ngrok needed.

### Option 2: HTTP + ngrok (same machine)

If you still want to use the HTTP endpoint (e.g. for Cursor or a browser client) and ngrok:

1. **Match the port** ngrok uses. Your ngrok forwards to `localhost:3001`, so start the server on **3001**:

   ```powershell
   uv run python server.py --http --port 3001
   ```

2. **Public URL**: `https://postsphenoid-soothingly-micha.ngrok-free.dev/sse` (always use the `/sse` path).

3. **ngrok free tier**: Requests from API clients (e.g. Cursor, Postman) can get ngrok’s “Visit Site” interstitial instead of your app. To avoid that, the client must send the header:
   - `ngrok-skip-browser-warning: true`  
   Not all MCP clients support custom headers; if yours doesn’t, the connection may fail with an “auth” or connection error.

4. **Claude Desktop**: Prefer **Option 1 (stdio)** for Claude. If your Claude build supports MCP over URL, you would set the server URL to `https://postsphenoid-soothingly-micha.ngrok-free.dev/sse`; the client must still send the `ngrok-skip-browser-warning` header if you’re on the free tier.

## Test with UI Inspector

1. Install or open [ui-inspector](https://github.com/idosal/ui-inspector).
2. For **HTTP**: set Server URL to `http://localhost:3000/sse`, Transport to **SSE**.
3. For **stdio**: choose **Stdio** and point to `uv run python server.py` (or your venv’s `python server.py`).
4. Connect and call the tools; UI resources render in the Tool Results panel.

## Docs

- [Python Server Walkthrough](https://mcpui.dev/guide/server/python/walkthrough)
- [mcp-ui-server Usage & Examples](https://mcpui.dev/guide/server/python/usage-examples)
- [MCP-UI SDK (GitHub)](https://github.com/MCP-UI-Org/mcp-ui)

## License

Apache-2.0.
