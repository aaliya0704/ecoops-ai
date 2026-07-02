import json
import requests


def classify_cloud_task(task_name: str) -> dict:
    """Uses a completely free, local Llama3 model running via Ollama

    to read a cloud task name and determine its delay safety.
    """
    # FIX: Corrected and completed local loopback address and endpoint path
    url = "http://127.0.0.1:11434/api/generate"

    system_prompt = (
        "You are an expert enterprise DevOps AI Agent. Analyze the given cloud software task name "
        "and determine if it is 'Mission-Critical' (must run instantly, affects live users, checkouts, production bugs) "
        "or 'Delay-Tolerant' (can be scheduled later, routine backups, analytics reports, data training, testing pipelines).\n\n"
        "Respond strictly in a valid JSON object matching this exact schema with no extra text or conversational pleasantries:\n"
        "{\n"
        '  "classification": "Mission-Critical" or "Delay-Tolerant",\n'
        '  "reason": "One short sentence explaining why"\n'
        "}"
    )

    # Structure the command request for your local Ollama engine
    payload = {
        "model": "llama3:8b",
        "prompt": f"{system_prompt}\n\nTask Name: {task_name}",
        "stream": False,  # Return the whole sentence at once instead of word-by-word
        "format": "json",  # FIX: Forces Ollama to strictly respond with structurally valid JSON
    }

    try:
        # Send the data packet over to your local running Llama3 instance
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()  # Check for HTTP request errors

        raw_output = response.json()["response"].strip()

        # FIX: Safe structured JSON parsing instead of raw string iteration
        parsed_data = json.loads(raw_output)

        # Normalize keys/fallbacks just in case
        category = parsed_data.get("classification", "Delay-Tolerant")
        reason = parsed_data.get("reason", "Processed by local AI cluster.")

        return {"classification": category, "reason": reason}

    except Exception as e:
        # Fallback safeguard in case your local Ollama app isn't open
        return {
            "classification": "Mission-Critical",
            "reason": f"Local AI engine connection offline ({str(e)}). Running instantly for standard core data safety.",
        }


# Local script validation test block
if __name__ == "__main__":
    test_job = "Run regular batch backup of historical user analytics databases"
    print("🤖 Testing Local Free LLM Classifier Agent...")
    print(classify_cloud_task(test_job))
