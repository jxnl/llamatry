# [Llamatry](https://github.com/jxnl/llamatry)

Llamatry is a Python package that simplifies the process of instrumenting the OpenAI API using OpenTelemetry. It allows you to monitor and trace the interactions with the OpenAI API, providing insights into the performance and behavior of your code. By leveraging OpenTelemetry, Llamatry supports various output formats, making it easy to integrate with your existing observability stack.

## Why?

Observability is essential for complex applications using large language models (LLMs), as it provides transparency, performance insights, and control over your data and even costs. By integrating observability into your LLM tooling, you can better understand their inner workings, optimize resource usage, and streamline your workflow. Owning your data and leveraging observability empowers you to take control of your AI application's performance.

## Features

* OpenTelemetry instrumentation for OpenAI API
* Supports tracing and monitoring of OpenAI API interactions
* Compatible with a wide range of output formats through OpenTelemetry
* Easy-to-use and straightforward setup process

## Installation

Install Llamatry using pip:

```bash
pip install llamatry
```

## Usage

To use Llamatry with the OpenAI API, follow these steps:

Import the necessary packages:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from llamatry import OpenAIInstrumentor

import openai
import os
```

Set up open telemetry:

```python
trace.set_tracer_provider(TracerProvider())
console_exporter = ConsoleSpanExporter()
span_processor = SimpleSpanProcessor(console_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
```

Set up OpenAI API:

```python
openai.api_key = os.environ["OPENAI_API_KEY"]
```

Instrument the OpenAI API using Llamatry:

```python
OpenAIInstrumentor().instrument()
```

Make API calls to the OpenAI API:

```python
response = openai.ChatCompletion.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ],
    max_tokens=50,
    temperature=0.5,
)
```

Console Export:

```json
{
    "name": "ChatCompletion.create",
    "context": {
        "trace_id": "0x6026b10ff364a1954df343ac2e292fd7",
        "span_id": "0x3f04991076717d88",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": "0x14abcdaf2d49f177",
    "start_time": "2023-05-09T20:32:10.674716Z",
    "end_time": "2023-05-09T20:32:11.827791Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "openai.create.model": "gpt-3.5-turbo",
        "openai.create.max_tokens": 500,
        "openai.create.temperature": 0.5,
        "openai.response.id": "chatcmpl-7EOIE4fVofq83WPl1HFNkDI6yBPZ8",
        "openai.response.created": 1683664330,
        "openai.response.model": "gpt-3.5-turbo-0301",
        "openai.usage.completion_tokens": 13,
        "openai.usage.prompt_tokens": 30,
        "openai.usage.total_tokens": 43
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.17.0",
            "service.name": "llamatry"
        },
        "schema_url": ""
    }
}
```

Traces and other information related to the OpenAI API calls will be output to the console. By using Llamatry, you can easily switch to other exporters supported by OpenTelemetry, such as Jaeger or Zipkin, to visualize and analyze the data in different ways.

## Decorator and Context Manager helpers

Llamatry provides a convenient tracing utility with both decorator and context manager support. This allows you to trace your functions and code blocks easily using the provided Trace class.

### Using the Trace decorator

To use the `Trace` class as a decorator, you can decorate your function using `@Trace.trace`. The function's name will be used as the span name by default. If you want to set a custom span name, you can provide it as an argument: `@Trace.trace("custom_span_name")`. By default if you decorate a function all arguments that are `(str, int, float, bool)` will be set as attributes.

```python
from llamatry import Trace

@Trace.trace
def your_function(a, b):
    # Your function implementation
    # a, b and automatically set as span attributes
    pass

@Trace.trace("custom_span_name")
def another_function():
    # Your function implementation
    pass

with Trace.span("custom_span_name") as span:
    # Your code block here
    span.set_attribute("foo", "bar")
    pass
```

### Using the Trace context manager

To use the Trace class as a context manager, use the `with` statement followed by `Trace.span("custom_span_name")`.

```python
from llamatry import Trace

with Trace.span("custom_span_name") as span:
    # Your code block here
    span.set_attribute("foo", "bar")
    pass
```

Using the `Trace` class in this way allows you to easily trace your functions and code blocks, providing better observability and understanding of the performance and behavior of your code.

## Documentation

For more information about OpenTelemetry, visit the [official OpenTelemetry Python documentation](https://opentelemetry-python.readthedocs.io/en/stable/).

For more information about the OpenAI API, visit the [official OpenAI API documentation](https://beta.openai.com/docs/).

## License

Llamatry is released under the [MIT License](https://opensource.org/licenses/MIT).
