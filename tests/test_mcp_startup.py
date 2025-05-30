#!/usr/bin/env python3
"""
Test script to verify MCP server can start properly
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🧪 Testing MCP Server Startup...")
print(f"📁 Current directory: {os.getcwd()}")
print(f"🔑 OPENAI_API_KEY present: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

try:
    # Import main to test initialization
    print("📦 Importing main module...")
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import main
    print("✅ MCP Server imported successfully!")
    
    # Test guardrail function
    print("🛡️ Testing guardrail function...")
    result = main.guardrail("Hello, this is a safe test message")
    print(f"📋 Guardrail result: {result}")
    
    print("🎉 MCP Server startup test completed successfully!")
    
except Exception as e:
    print(f"❌ Error during startup test: {e}")
    print(f"📚 Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
