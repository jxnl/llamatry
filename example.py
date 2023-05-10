import os
import openai
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    ConsoleMetricExporter,
)

# Set up OpenTelemtry Metrics to export to console
reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

# Set up OpenTelemetry Tracing to export to console
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# Set up OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Instrument the OpenAI API
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from llamatry import tracer, OpenAIInstrumentor

OpenAIInstrumentor().instrument()
RequestsInstrumentor().instrument()


# Use the OpenAI API
@tracer.wrap("entry_point")
def call(prompt):
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.5,
    )


if __name__ == "__main__":
    call("What is the meaning of life in a short sentence?")
