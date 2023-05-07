import os
import openai
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from llamatry import OpenAIInstrumentor

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Instrument the OpenAI API
OpenAIInstrumentor().instrument()
RequestsInstrumentor().instrument()


# Use the OpenAI API
def call(prompt):
    # get the current span 
    span = trace.get_current_span()
    span.set_attribute("openai.prompt", prompt)
    response = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.5,
    )
    span.set_attribute("openai.response", response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    with trace.get_tracer_provider().get_tracer(__name__).start_as_current_span("main"):
        call("What is the meaning of life in a short sentence?")
        call("What is the meaning of death in a long paragraph?")