# Minimal MCP Server (Python)

This is a minimal Model Context Protocol (MCP) server using the official Python SDK.

## Features
- Tool: `guardrail(context: str) -> bool` — Checks if the provided context is safe (no code injection or harmful content). Returns `True` if safe, `False` otherwise.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python main.py
   ```

## Test with MCP Inspector

To test and explore your server with a GUI:
```bash
mcp dev main.py
```

## Install in Claude Desktop

To use this MCP server as a tool in Claude Desktop:
1. Make sure you have [Claude Desktop](https://claude.ai/desktop) installed.
2. In your terminal, run:
   ```bash
   mcp install main.py
   ```
3. The server will appear as a tool in Claude Desktop, ready to use.

## References
- [Model Context Protocol Docs](https://modelcontextprotocol.io/docs/)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/desktop) 