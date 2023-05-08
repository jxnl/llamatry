import os
import openai
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from llamatry import OpenAICompletionInstrumentor, Trace

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Instrument the OpenAI API
OpenAICompletionInstrumentor().instrument()
RequestsInstrumentor().instrument()


# Use the OpenAI API
@Trace.trace
def call(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.5,
    )
    # add attributes to the span to capture the prompt and response
    # this will be exported to the console but one can imagine this doing into
    # a database or other storage for search or review later
    span = trace.get_current_span()
    span.set_attribute("openai.prompt", prompt)
    span.set_attribute("openai.response", response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    call("What is the meaning of life in a short sentence?")

    with Trace.span("span") as span:
        call("What is the meaning of life in a short sentence?")
        span.set_attribute("foo", "bar")
