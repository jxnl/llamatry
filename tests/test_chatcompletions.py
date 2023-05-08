import os
import openai
import pytest
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from llamatry import OpenAICompletionInstrumentor

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Instrument the OpenAI API
OpenAICompletionInstrumentor().instrument()


@pytest.mark.asyncio
async def test_chat_acreate():
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What is the meaning of life?",
            },
        ],
        max_tokens=5,
        temperature=0.5,
        stream=False,
    )
    assert response is not None
    assert response["choices"][0]["message"]["content"] is not None


@pytest.mark.asyncio
async def test_chat_acreate_stream():
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What is the meaning of life in a short sentence?",
            },
        ],
        max_tokens=5,
        temperature=0.5,
        stream=True,
    )
    assert response is not None
    async for obj in response:
        delta = obj["choices"][0]["delta"]
        if "content" in delta:
            assert delta["content"] is not None


def test_chat_create_stream():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What is the meaning of life in a short sentence?",
            },
        ],
        max_tokens=5,
        temperature=0.5,
        stream=True,
    )
    assert response is not None
    for obj in response:
        delta = obj["choices"][0]["delta"]
        if "content" in delta:
            assert delta["content"] is not None


def test_chat_create():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What is the meaning of life in a short sentence?",
            },
        ],
        max_tokens=5,
        temperature=0.5,
    )
    assert response is not None
    assert response["choices"][0]["message"]["content"] is not None
