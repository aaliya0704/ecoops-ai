import requests
import json


def classify_cloud_task(task_name: str) -> dict:
    """
    Uses a completely free, local Llama3 model running via Ollama
    to read a cloud task name and determine its delay safety.
    """
    url = "http://localhost:11434/api/generate"

    system_prompt = (
        "You are an expert enterprise DevOps AI Agent. Analyze the given cloud software task name "
        "and determine if it is 'Mission-Critical' (must run instantly, affects live users, checkouts, production bugs) "
        "or 'Delay-Tolerant' (can be scheduled later, routine backups, analytics reports, data training, testing pipelines).\n\n"
        "Respond strictly in this exact format with no extra text or pleasantries:\n"
        "Category: <Mission-Critical or Delay-Tolerant>\n"
        "Reason: <One short sentence explaining why>"
    )

    # Structure the command request for your local Ollama engine
    payload = {
        "model": "llama3:8b",
        "prompt": f"{system_prompt}\n\nTask Name: {task_name}",
        "stream": False,  # Return the whole sentence at once instead of word-by-word
    }

    try:
        # Send the data packet over to your local running Llama3 instance
        response = requests.post(url, json=payload, timeout=10)
        raw_output = response.json()["response"].strip()

        # Parse the output text back into structured data for your dashboard
        lines = raw_output.split("\n")
        category = "Delay-Tolerant"  # Default fallback safe state
        reason = "Processed by local AI cluster."

        for line in lines:
            if "Category:" in line:
                category = line.replace("Category:", "").strip()
            if "Reason:" in line:
                reason = line.replace("Reason:", "").strip()

        return {"classification": category, "reason": reason}

    except Exception as e:
        # Fallback safeguard in case your local Ollama app isn't open
        return {
            "classification": "Mission-Critical",
            "reason": "Local AI engine connection offline. Running instantly for standard core data safety.",
        }


# Local script validation test block
if __name__ == "__main__":
    test_job = "Run regular batch backup of historical user analytics databases"
    print("🤖 Testing Local Free LLM Classifier Agent...")
    print(classify_cloud_task(test_job))
