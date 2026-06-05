import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


def ask_ollama(messages):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "messages": messages,
                "stream": False
            },
            timeout=60
        )

        print("OLLAMA RAW STATUS:", r.status_code)
        print("OLLAMA RAW TEXT:", r.text)

        data = r.json()


        if "message" not in data:
            return ""

        return data["message"].get("content", "")

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return ""