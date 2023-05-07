import functools
import logging
from typing import Collection
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import SpanKind
import openai

logger = logging.getLogger(__name__)

class OpenAIInstrumentor(BaseInstrumentor):

    def _instrument(self, **kwargs):
        self._original_create = openai.ChatCompletion.create
        self._original_acreate = openai.ChatCompletion.acreate
        openai.ChatCompletion.create = self._trace_create(self._original_create)
        openai.ChatCompletion.acreate = self._trace_acreate(self._original_acreate)

    def _uninstrument(self, **kwargs):
        openai.ChatCompletion.create = self._original_create
        openai.ChatCompletion.acreate = self._original_acreate
    
    def instrumentation_dependencies(self) -> Collection[BaseInstrumentor]:
        return []

    @staticmethod
    def _set_attributes(span, kwargs, response):
        for key, value in kwargs.items():
            if isinstance(value, (str, bool, float, int)):
                span.set_attribute(f"openai.create.{key}", value)
        
        usage = response.get("usage", {})
        span.set_attribute("openai.response.id", response.get("id", ""))
        span.set_attribute("openai.response.created", response.get("created", 0))
        span.set_attribute("openai.usage.prompt_tokens", usage.get("prompt_tokens", 0))
        span.set_attribute("openai.usage.completion_tokens", usage.get("completion_tokens", 0))
        span.set_attribute("openai.usage.total_tokens", usage.get("total_tokens", 0))

    def _trace_create(self, original_create):
        @functools.wraps(original_create)
        def wrapper(*args, **kwargs):
            stream = kwargs.get("stream", False)
            if stream:
                logger.warning("stream=True is not implemented for tracing.")
                return original_create(*args, **kwargs)

            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span("openai.ChatCompletion.create", kind=SpanKind.CLIENT) as span:
                response = original_create(*args, **kwargs)
                self._set_attributes(span, kwargs, response)
            return response

        return wrapper

    def _trace_acreate(self, original_acreate):
        @functools.wraps(original_acreate)
        async def wrapper(*args, **kwargs):
            stream = kwargs.get("stream", False)
            if stream:
                logger.warning("stream=True is not implemented for tracing.")
                return await original_acreate(*args, **kwargs)

            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span("openai.ChatCompletion.acreate", kind=SpanKind.CLIENT) as span:
                response = await original_acreate(*args, **kwargs)
                self._set_attributes(span, kwargs, response)
            return response

        return wrapper
