import os

import requests


MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-latest")


def complete(messages):
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise RuntimeError("CLAUDE_API_KEY is not configured")
    system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
    user_messages = [item for item in messages if item["role"] != "system"]
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={"model": MODEL, "max_tokens": 700, "system": system, "messages": user_messages},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["content"][0]["text"]
