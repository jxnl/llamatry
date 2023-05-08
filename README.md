# Llamatry

Llamatry is a Python package that simplifies the process of instrumenting the OpenAI API using OpenTelemetry. It allows you to monitor and trace the interactions with the OpenAI API, providing insights into the performance and behavior of your code. By leveraging OpenTelemetry, Llamatry supports various output formats, making it easy to integrate with your existing observability stack.

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
import os
import openai
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from llamatry import OpenAICompletionInstrumentor
```

Set up OpenTelemetry:

## Configure logging

```python
logging.basicConfig(level=logging.WARNING)
```

## Set up OpenTelemetry

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
OpenAICompletionInstrumentor().instrument()
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

Traces and other information related to the OpenAI API calls will be output to the console. By using Llamatry, you can easily switch to other exporters supported by OpenTelemetry, such as Jaeger or Zipkin, to visualize and analyze the data in different ways.

## Documentation

For more information about OpenTelemetry, visit the [official OpenTelemetry Python documentation](https://opentelemetry-python.readthedocs.io/en/stable/).

For more information about the OpenAI API, visit the [official OpenAI API documentation](https://beta.openai.com/docs/).

## License

Llamatry is released under the [MIT License](https://opensource.org/licenses/MIT).
