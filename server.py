"""
Python MCP server with MCP-UI resources.

Uses FastMCP and mcp-ui-server to expose tools that return interactive UI
resources (HTML, external URLs) for MCP UI–capable hosts.

Docs: https://mcpui.dev/guide/server/python/walkthrough
"""
import argparse
from mcp.server.fastmcp import FastMCP
from mcp_ui_server import create_ui_resource
from mcp_ui_server.core import UIResource

mcp = FastMCP("mcp-ui-python-server")


@mcp.tool()
def greet() -> list[UIResource]:
    """A simple greeting tool that returns a UI resource."""
    ui_resource = create_ui_resource({
        "uri": "ui://greeting/simple",
        "content": {
            "type": "rawHtml",
            "htmlString": """
                <div style="padding: 20px; text-align: center; font-family: Arial, sans-serif;">
                    <h1 style="color: #2563eb;">Hello from Python MCP Server!</h1>
                    <p>This UI resource was generated server-side using mcp-ui-server.</p>
                </div>
            """,
        },
        "encoding": "text",
    })
    return [ui_resource]


@mcp.tool()
def show_dashboard() -> list[UIResource]:
    """Display a sample dashboard with metrics."""
    dashboard_html = """
    <div style="padding: 20px; font-family: Arial, sans-serif;">
        <h1>Server Dashboard</h1>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 20px;">
            <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 16px;">
                <h3 style="margin-top: 0; color: #0369a1;">Active Connections</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 0; color: #0c4a6e;">42</p>
            </div>
            <div style="background: #f0fdf4; border: 1px solid #22c55e; border-radius: 8px; padding: 16px;">
                <h3 style="margin-top: 0; color: #15803d;">CPU Usage</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 0; color: #14532d;">23%</p>
            </div>
            <div style="background: #fefce8; border: 1px solid #eab308; border-radius: 8px; padding: 16px;">
                <h3 style="margin-top: 0; color: #a16207;">Memory Usage</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 0; color: #713f12;">67%</p>
            </div>
        </div>
    </div>
    """
    ui_resource = create_ui_resource({
        "uri": "ui://dashboard/main",
        "content": {
            "type": "rawHtml",
            "htmlString": dashboard_html,
        },
        "encoding": "text",
    })
    return [ui_resource]


@mcp.tool()
def show_external_site() -> list[UIResource]:
    """Display an external website in an iframe."""
    ui_resource = create_ui_resource({
        "uri": "ui://external/example",
        "content": {
            "type": "externalUrl",
            "iframeUrl": "https://example.com",
        },
        "encoding": "text",
    })
    return [ui_resource]


@mcp.tool()
def show_interactive_demo() -> list[UIResource]:
    """Show an interactive demo with buttons that send intents and tool calls."""
    interactive_html = """
    <div style="padding: 20px; font-family: Arial, sans-serif;">
        <h2>Interactive Demo</h2>
        <p>Click the buttons below to send different types of actions back to the parent:</p>

        <div style="margin: 10px 0;">
            <button onclick="sendIntent('user_action', {type: 'button_click', id: 'demo'})"
                    style="background: #2563eb; color: white; padding: 8px 16px; border: none; border-radius: 4px; margin: 5px; cursor: pointer;">
                Send Intent
            </button>
            <button onclick="sendToolCall('get_data', {source: 'ui'})"
                    style="background: #059669; color: white; padding: 8px 16px; border: none; border-radius: 4px; margin: 5px; cursor: pointer;">
                Call Tool
            </button>
        </div>

        <div id="status" style="margin-top: 20px; padding: 10px; background: #f3f4f6; border-radius: 4px;">
            Ready - click a button to see the action
        </div>
    </div>

    <script>
        function sendIntent(intent, params) {
            const status = document.getElementById('status');
            status.innerHTML = `<strong>Intent sent:</strong> ${intent}<br><strong>Params:</strong> ${JSON.stringify(params)}`;

            if (window.parent) {
                window.parent.postMessage({
                    type: 'intent',
                    payload: { intent: intent, params: params }
                }, '*');
            }
        }

        function sendToolCall(toolName, params) {
            const status = document.getElementById('status');
            status.innerHTML = `<strong>Tool call:</strong> ${toolName}<br><strong>Params:</strong> ${JSON.stringify(params)}`;

            if (window.parent) {
                window.parent.postMessage({
                    type: 'tool',
                    payload: { toolName: toolName, params: params }
                }, '*');
            }
        }
    </script>
    """
    ui_resource = create_ui_resource({
        "uri": "ui://demo/interactive",
        "content": {
            "type": "rawHtml",
            "htmlString": interactive_html,
        },
        "encoding": "text",
    })
    return [ui_resource]


def main() -> None:
    parser = argparse.ArgumentParser(description="MCP UI Python Server")
    parser.add_argument(
        "--http",
        action="store_true",
        help="Use HTTP (SSE) transport instead of stdio",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port for HTTP transport (default: 3000)",
    )
    args = parser.parse_args()

    if args.http:
        print("Starting MCP server on HTTP (SSE transport)")
        mcp.settings.port = args.port
        mcp.run(transport="sse")
    else:
        print("Starting MCP server with stdio transport")
        mcp.run()


if __name__ == "__main__":
    main()
