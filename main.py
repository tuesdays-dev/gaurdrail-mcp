from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tuesdays.dev")

@mcp.tool()
def guardrail(context: str) -> bool:
    """Before running any tool pass the context and the tool request to this tool to check if it is safe.
    If it is not safe, it returns False so do NOT continue, otherwise it returns True so continue."""
    suspicious_keywords = [
        'import', 'exec', 'eval', 'os.system', 'subprocess', 'open(', 'write(', 'read(',
        '__import__', 'pickle', 'input(', 'compile(', 'globals()', 'locals()', 'os.environ',
        'sys.modules', 'shutil', 'rm -rf', 'del ', 'kill', 'fork', 'spawn', 'socket', 'ftp',
        'base64', 'decode', 'encode', 'b64', 'http', 'https', 'curl', 'wget', 'bash', 'zsh',
        'sh ', 'cmd', 'powershell', 'registry', 'reg ', 'keylogger', 'token', 'secret', 'password'
    ]
    lowered = context.lower()
    for keyword in suspicious_keywords:
        if keyword in lowered:
            return False
    return True

# Test
@mcp.prompt()
def write_email(recipient: str, subject: str, tone: str = "professional") -> str:
    """Generate an email template"""
    return f"""
    Write an email to {recipient} with the subject "{subject}".
    Use a {tone} tone.
    Include appropriate greeting and closing.
    """

if __name__ == "__main__":
    mcp.run()
