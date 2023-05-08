import functools
from typing import Collection
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import SpanKind
import openai


class OpenAICompletionInstrumentor(BaseInstrumentor):
    def _instrument(self, **kwargs):
        self._original_chatcompletion_create = openai.ChatCompletion.create
        self._original_chatcompletion_acreate = openai.ChatCompletion.acreate
        self._original_create = openai.Completion.create
        self._original_acreate = openai.Completion.acreate
        openai.ChatCompletion.create = self._trace_create(
            self._original_chatcompletion_create
        )
        openai.ChatCompletion.acreate = self._trace_acreate(
            self._original_chatcompletion_acreate
        )
        openai.Completion.create = self._trace_create(self._original_create)
        openai.Completion.acreate = self._trace_acreate(self._original_acreate)

    def _uninstrument(self, **kwargs):
        openai.ChatCompletion.create = self._original_chatcompletion_create
        openai.ChatCompletion.acreate = self._original_chatcompletion_acreate
        openai.Completion.create = self._original_completion_create
        openai.Completion.acreate = self._original_completion_acreate

    def instrumentation_dependencies(self) -> Collection[BaseInstrumentor]:
        return []

    @staticmethod
    def _set_span_attributes(span, kwargs, response):
        """
        Set attributes on the span for the prompt and response, purposefully
        ignoring the prompt and response attributes as they are may be too large

        :param span: the span to set attributes on
        :param kwargs: the kwargs passed to the create method
        :param response: the response from the create method
        """
        for key, value in kwargs.items():
            if isinstance(value, (str, bool, float, int)) and key != "prompt":
                span.set_attribute(f"openai.create.{key}", value)

        usage = response.get("usage", {})
        span.set_attribute("openai.response.id", response.get("id", ""))
        span.set_attribute("openai.response.created", response.get("created", 0))

        # only set these attributes if the response is a stream since the are
        # not present in the non-streaming response
        if kwargs.get("stream", False):
            span.set_attribute(
                "openai.usage.prompt_tokens", usage.get("prompt_tokens", None)
            )
            span.set_attribute(
                "openai.usage.completion_tokens", usage.get("completion_tokens", None)
            )
            span.set_attribute(
                "openai.usage.total_tokens", usage.get("total_tokens", None)
            )

    def _trace_create(self, original_create):
        @functools.wraps(original_create)
        def wrapper(*args, **kwargs):
            stream = kwargs.get("stream", False)
            tracer = trace.get_tracer(__name__)

            with tracer.start_as_current_span(
                "openai.ChatCompletion.create", kind=SpanKind.CLIENT
            ) as span:
                if stream:

                    def stream_wrapper():
                        first_chunk = True
                        for resp in original_create(*args, **kwargs):
                            if first_chunk:
                                self._set_span_attributes(span, kwargs, resp)
                                first_chunk = False
                            yield resp

                    return stream_wrapper()
                else:
                    response = original_create(*args, **kwargs)
                    self._set_span_attributes(span, kwargs, response)
                    return response

        return wrapper

    def _trace_acreate(self, original_acreate):
        @functools.wraps(original_acreate)
        async def wrapper(*args, **kwargs):
            stream = kwargs.get("stream", False)
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(
                "openai.ChatCompletion.acreate", kind=SpanKind.CLIENT
            ) as span:
                response = await original_acreate(*args, **kwargs)
                if stream:

                    async def stream_wrapper():
                        first_chunk = True
                        async for resp in response:
                            if first_chunk:
                                self._set_span_attributes(span, kwargs, resp)
                                first_chunk = False
                            yield resp

                    return stream_wrapper()
                else:
                    self._set_span_attributes(span, kwargs, response)
                    return response  # type: ignore

        return wrapper
