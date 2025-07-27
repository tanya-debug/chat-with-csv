import ollama
import json

def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to the local model and returns its response text.
    Ensures the output is a clean string and provides proper JSON on error.
    """
    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        # Return a valid JSON string even on failure
        error_json = {
            "chart_needed": False,
            "response": f"Error communicating with the model: {str(e)}"
        }
        return json.dumps(error_json, ensure_ascii=False)
