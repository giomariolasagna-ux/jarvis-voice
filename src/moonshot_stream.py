import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url="https://api.moonshot.ai/v1"
)

def stream_moonshot(messages):
    stream = client.chat.completions.create(
        model="kimi-k2-thinking-turbo",
        messages=messages,
        stream=True,
        temperature=0.4,
        max_tokens=600
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                yield delta.content
