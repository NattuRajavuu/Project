import os


MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _client():
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return OpenAI(api_key=api_key)


def complete(messages):
    response = _client().chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content or ""


def stream(messages):
    stream_response = _client().chat.completions.create(model=MODEL, messages=messages, stream=True)
    for chunk in stream_response:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
