import os

import requests


MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def complete(messages):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    prompt = "\n".join(f"{item['role']}: {item['content']}" for item in messages)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    response = requests.post(
        url,
        params={"key": api_key},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
