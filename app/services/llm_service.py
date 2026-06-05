import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def call_ollama(messages: list):

    prompt = ""

    for m in messages:
        prompt += f"{m['role']}: {m['content']}\n"

    prompt += "assistant:"

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return res.json()["response"]
    print(res)

def extract_json(text: str):
    if not text:
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return None
    return None