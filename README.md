# Guardrail MCP Server

This project combines a minimal Model Context Protocol (MCP) server with a flexible AI client that supports both OpenAI and Ollama APIs.

## Components

### MCP Server
- **Tool**: `guardrail(context: str) -> Dict[str, Any]` — Uses OpenAI to intelligently analyze context for security risks, code injection attempts, and harmful content. Returns a dictionary with:
  - `safe`: Boolean indicating if the context is safe
  - `reason`: String explanation if unsafe (empty if safe)
- **Fail-safe**: Returns `safe: False` when OpenAI is unavailable or errors occur

### AI Client Library
- **Multi-provider support**: Works with both OpenAI and Ollama APIs
- **Environment variable configuration**: Uses `.env` file for secure API key management
- **JSON response formatting**: Automatically requests and parses JSON responses
- **Context support**: Always includes context in prompts for better AI responses
- **Error handling**: Comprehensive error handling for network and parsing issues

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your-openai-api-key-here
# OLLAMA_BASE_URL=http://localhost:11434  # optional
# OLLAMA_MODEL=llama2                     # optional
```

### 3. Run the MCP Server
```bash
python main.py
```

### 4. Use the AI Client
```python
from ai_client import AIApp

# Using OpenAI (requires OPENAI_API_KEY in .env)
app = AIApp()
app.setup_openai()
result = app.query("What is Python?", "Programming languages discussion")

# Using Ollama (uses defaults or env vars)
app = AIApp()
app.setup_ollama()
result = app.query("What is Python?", "Programming languages discussion")
```

### 5. Run Integration Tests
```bash
# Test AI client with both OpenAI and Ollama
python tests/test_ai_client.py

# Test guardrail functionality
python tests/test_guardrail.py

# Test MCP server startup
python tests/test_mcp_startup.py
```
<!-- For now -->
## AI Client Usage

### Environment Variables
The AI client uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI)
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Ollama model name (default: llama2)

### Response Format
All responses follow this structure:
```json
{
  "success": true,
  "response": { /* parsed JSON from AI */ },
  "raw_response": "original response string",
  "usage": { /* token usage info (OpenAI only) */ }
}
```

### Error Handling
Errors are returned in this format:
```json
{
  "success": false,
  "error": "Description of the error"
}
```

## Examples

### AI Client Integration Test
Run the AI client integration test:
```bash
python tests/test_ai_client.py
```

This demonstrates both OpenAI and Ollama integration with proper error handling.

### Guardrail Testing
Test the guardrail functionality:
```bash
python tests/test_guardrail.py
```

This tests various scenarios including:
- Safe requests
- Code injection attempts
- File access attempts
- SQL injection attempts

### Example Guardrail Response
```json
{
  "safe": false,
  "reason": "Detected potential command injection attempt with destructive system commands"
}
```

## MCP Server Testing

### Test with MCP Inspector
```bash
mcp dev main.py
```

### Install in Claude Desktop

#### Option 1: Direct Python (Recommended)
```json
{
  "mcpServers": {
    "tuesdays.dev": {
      "command": "python",
      "args": [
        "/path/to/your/guardrail-mcp/main.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Option 2: UV with Requirements
```json
{
  "mcpServers": {
    "tuesdays.dev": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--with-requirements", "/path/to/your/guardrail-mcp/requirements.txt",
        "python", "/path/to/your/guardrail-mcp/main.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Option 3: UV Basic (May have dependency issues)
```json
{
  "mcpServers": {
    "tuesdays.dev": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--with", "mcp[cli]",
        "mcp", "run",
        "/path/to/your/guardrail-mcp/main.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Note**: Replace `/path/to/your/guardrail-mcp/` with the actual path to your project.

## Troubleshooting

### MCP Server Connection Issues
If you see connection errors in Claude Desktop like:
```
Server transport closed unexpectedly
Server disconnected
```

**Most likely cause**: Missing `OPENAI_API_KEY` environment variable.

**Solution**:
1. Make sure you have a `.env` file in the project root
2. Add your OpenAI API key: `OPENAI_API_KEY=your-api-key-here`
3. Restart Claude Desktop

**Test server startup**:
```bash
python tests/test_mcp_startup.py
```

This will show detailed startup information and help identify configuration issues.

### Expected Behavior
- **With API key**: ✅ Full AI-powered guardrail functionality
- **Without API key**: ⚠️ Server runs but marks all content as unsafe

## Project Structure
```
.
├── ai_client.py          # AI client library
├── main.py              # MCP server with AI-powered guardrail
├── tests/
│   ├── test_ai_client.py # AI client integration test
│   ├── test_guardrail.py # Guardrail testing script
│   └── test_mcp_startup.py # MCP server startup test
├── .env.example         # Environment template
├── requirements.txt     # Dependencies
└── README.md           # This file
```


## References
- [Model Context Protocol Docs](https://modelcontextprotocol.io/docs/)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/desktop)
