import os
import openai
import pytest
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from llamatry import OpenAIInstrumentor

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Instrument the OpenAI API
OpenAIInstrumentor().instrument()


@pytest.mark.asyncio
async def test_completion_acreate():
    response = await openai.Completion.acreate(
        engine="text-ada-001",
        prompt="Respond with 'Hello!'",
        max_tokens=5,
        temperature=0.5,
        n=1,
        stream=False,
    )
    assert response is not None
    assert response["choices"][0]["text"] is not None


@pytest.mark.asyncio
async def test_completion_acreate_stream():
    response = await openai.Completion.acreate(
        engine="text-ada-001",
        prompt="Respond with 'Hello!'",
        max_tokens=5,
        temperature=0.5,
        n=1,
        stream=True,
    )
    assert response is not None
    async for resp in response:
        assert resp["choices"][0]["text"] is not None


def test_completion_create():
    response = openai.Completion.create(
        engine="text-ada-001",
        prompt="Respond with 'Hello!'",
        max_tokens=5,
        temperature=0.5,
        n=1,
        stream=False,
    )
    assert response is not None
    assert response["choices"][0]["text"] is not None


def test_completion_create_stream():
    response = openai.Completion.create(
        engine="text-ada-001",
        prompt="Respond with 'Hello!'",
        max_tokens=5,
        temperature=0.5,
        n=1,
        stream=True,
    )
    assert response is not None
    for resp in response:
        assert resp["choices"][0]["text"] is not None
