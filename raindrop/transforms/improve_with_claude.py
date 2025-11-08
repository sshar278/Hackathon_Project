from dotenv import load_dotenv
import os
load_dotenv()
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

import json
import requests

def call_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-5-sonnet-latest",
        "max_tokens": 800,
        "system": "Return strict JSON only.",
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post("https://api.anthropic.com/v1/messages",
                      headers=headers, json=payload)
    text = r.json().get("content", [{}])[0].get("text", "{}")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "explanation": "Error parsing Claude response",
            "patch": ""
        }

def main(meta):
    with open("raindrop/prompts/improve_prompt.txt") as f:
        prompt = f.read().format(**meta)
    result = call_claude(prompt)
    meta.update(result)
    return meta

