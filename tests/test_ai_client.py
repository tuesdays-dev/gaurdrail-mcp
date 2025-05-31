import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to import ai_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_client import AIApp

# Example usage
if __name__ == "__main__":
    # Example with OpenAI (uses OPENAI_API_KEY from environment)
    print("=== OpenAI Example ===")
    app = AIApp()
    
    try:
        app.setup_openai()  # Will use OPENAI_API_KEY from .env
        
        # Example query
        prompt = "What are the main benefits of renewable energy?"
        context = "We are discussing environmental sustainability and energy policy."
        
        result = app.query(prompt, context)
        
        if result["success"]:
            print("Success!")
            print("Response:", json.dumps(result["response"], indent=2))
        else:
            print("Error:", result["error"])
            
    except ValueError as e:
        print(f"OpenAI setup error: {e}")
        print("Make sure to set OPENAI_API_KEY in your .env file")
    
    print("\n" + "="*50 + "\n")
    
    # Example with Ollama (uses environment variables or defaults)
    print("=== Ollama Example ===")
    app = AIApp()
    app.setup_ollama("http://localhost:11434", "llama3.2:latest")  # Use available model
    
    # Example query
    prompt = "List 3 programming languages and their primary use cases"
    context = "We are evaluating technology choices for a new software project."
    
    result = app.query(prompt, context)
    
    if result["success"]:
        print("Response:", json.dumps(result["response"], indent=2))
    else:
        print("Error:", result["error"])
