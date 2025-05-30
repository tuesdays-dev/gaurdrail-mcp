from mcp.server.fastmcp import FastMCP
import json
import sys
from typing import Dict, Any

# Try to import AI client with graceful fallback
try:
    from ai_client import AIApp
    AI_CLIENT_AVAILABLE = True
except ImportError as e:
    print(f"❌ Warning: AI client not available: {e}", file=sys.stderr)
    print("ℹ️  Install missing dependencies: pip install requests python-dotenv", file=sys.stderr)
    AI_CLIENT_AVAILABLE = False
    AIApp = None

mcp = FastMCP("tuesdays.dev")

# Initialize AI client for guardrail checks
if AI_CLIENT_AVAILABLE and AIApp:
    ai_app = AIApp()
    try:
        ai_app.setup_openai()
        print("✅ OpenAI client initialized successfully", file=sys.stderr)
    except ValueError as e:
        print(f"⚠️  Warning: OpenAI setup failed: {e}", file=sys.stderr)
        print("ℹ️  Guardrail will return 'unsafe' for all requests when OpenAI is unavailable", file=sys.stderr)
        print("ℹ️  To fix: Set OPENAI_API_KEY in your .env file", file=sys.stderr)
        ai_app = None
    except Exception as e:
        print(f"❌ Unexpected error during OpenAI setup: {e}", file=sys.stderr)
        ai_app = None
else:
    print("❌ Dependencies missing - guardrail will return 'unsafe' for all requests", file=sys.stderr)
    ai_app = None

@mcp.tool()
def guardrail(context: str) -> Dict[str, Any]:
    """On running any tool and on each function, pass the request with its parameters to guardrail to check if it is safe.
    Returns a dictionary with 'safe' (bool) and 'reason' (str) and do NOT continue, if not safe.
    Otherwise it returns True so continue."""
    
    if ai_app is not None:
        # Use OpenAI for intelligent safety analysis
        try:
            system_context = """You are a security guardrail system. Analyze the provided context for potential security risks, code injection attempts, harmful content, or malicious activities.
            
Your task is to determine if the context is SAFE or UNSAFE.
            
Consider these risk factors:
- Code injection attempts (SQL injection, command injection, script injection)
- Attempts to access sensitive files or system resources
- Malicious code execution attempts
- Attempts to bypass security measures
- Harmful or destructive commands
- Unauthorized data access attempts
- Social engineering attempts
- Attempts to escalate privileges

Respond with a JSON object containing:
- "safe": true/false
- "reason": "brief explanation if unsafe, empty string if safe"

Be conservative - when in doubt, mark as unsafe."""
            
            result = ai_app.query(
                prompt=f"Analyze this context for security risks: {context}",
                context=system_context
            )
            
            if result["success"]:
                response = result["response"]
                return {
                    "safe": response.get("safe", False),
                    "reason": response.get("reason", "")
                }
            else:
                # AI failed, return unsafe
                print(f"⚠️  AI analysis failed for context: {context[:50]}...", file=sys.stderr)
                return {"safe": False, "reason": "AI analysis failed - assuming unsafe"}
                
        except Exception as e:
            print(f"❌ AI guardrail error: {e}", file=sys.stderr)
            return {"safe": False, "reason": "Guardrail system error - assuming unsafe"}
    else:
        # No AI available, return unsafe
        print(f"⚠️  No AI client available, marking as unsafe: {context[:50]}...", file=sys.stderr)
        return {"safe": False, "reason": "AI guardrail unavailable - set OPENAI_API_KEY"}

# Test
@mcp.prompt()
def fix_grammer_or_translate(text: str, language: str = "english") -> str:
    """Fix this text gramatically or translate it to {language}"""
    return f"""Fix this text gramatically or translate it to {language}"""

if __name__ == "__main__":
    mcp.run()
