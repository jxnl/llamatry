import functools
from typing import Collection
from opentelemetry import trace
from opentelemetry import metrics
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
import openai

tracer = trace.get_tracer("llamatry")


class OpenAIInstrumentor(BaseInstrumentor):
    def _instrument(self, **kwargs):
        self._original_chatcompletion_create = openai.ChatCompletion.create
        self._original_chatcompletion_acreate = openai.ChatCompletion.acreate
        self._original_create = openai.Completion.create
        self._original_acreate = openai.Completion.acreate
        self._original_embeddings_create = openai.Embedding.create
        self._original_embeddings_acreate = openai.Embedding.acreate

        openai.ChatCompletion.create = self._trace_create(
            self._original_chatcompletion_create
        )
        openai.ChatCompletion.acreate = self._trace_acreate(
            self._original_chatcompletion_acreate
        )
        openai.Completion.create = self._trace_create(self._original_create)
        openai.Completion.acreate = self._trace_acreate(self._original_acreate)
        openai.Embedding.create = self._trace_create(self._original_embeddings_create)
        openai.Embedding.acreate = self._trace_acreate(
            self._original_embeddings_acreate
        )

    def _uninstrument(self, **kwargs):
        openai.ChatCompletion.create = self._original_chatcompletion_create
        openai.ChatCompletion.acreate = self._original_chatcompletion_acreate
        openai.Completion.create = self._original_completion_create
        openai.Completion.acreate = self._original_completion_acreate
        openai.Embedding.create = self._original_embeddings_create
        openai.Embedding.acreate = self._original_embeddings_acreate

    def instrumentation_dependencies(self) -> Collection[BaseInstrumentor]:
        return []

    @staticmethod
    def _handle_attributes(span, kwargs, response):
        """
        Set attributes on the span for the prompt and response, purposefully
        ignoring the prompt and response attributes as they are may be too large

        :param span: the span to set attributes on
        :param kwargs: the kwargs passed to the create method
        :param response: the response from the create method
        """
        for key, value in kwargs.items():
            if isinstance(value, (str, bool, float, int)) and key != "prompt":
                # Don't set the prompt attribute as it may be too large
                span.set_attribute(f"openai.create.{key}", value)

        for key in ["id", "created", "model"]:
            if key in response:
                span.set_attribute(f"openai.response.{key}", response[key])

        usage = response.get("usage", None)
        model = response.get("model", "__unknown__")
        if usage:
            for key in ["completion_tokens", "prompt_tokens", "total_tokens"]:
                if key in usage:
                    span.set_attribute(f"openai.usage.{key}", usage[key])

                    # Create a counter for the usage metric for each type of prompt token usage
                    meter = metrics.get_meter(f"openai.{model}")
                    counter = meter.create_counter(
                        name=key,
                        description=f"OpenAI {model} {key}",
                    )
                    counter.add(usage[key])

    def _trace_create(self, original_create):
        @functools.wraps(original_create)
        def wrapper(*args, **kwargs):
            stream = kwargs.get("stream", False)

            with tracer.start_as_current_span(
                f"openai.{original_create.__qualname__}",
            ) as span:
                if stream:

                    def stream_wrapper():
                        first_chunk = True
                        for resp in original_create(*args, **kwargs):
                            if first_chunk:
                                self._handle_attributes(span, kwargs, resp)
                                first_chunk = False
                            yield resp

                    return stream_wrapper()
                else:
                    response = original_create(*args, **kwargs)
                    self._handle_attributes(span, kwargs, response)
                    return response

        return wrapper

    def _trace_acreate(self, original_acreate):
        @functools.wraps(original_acreate)
        async def wrapper(*args, **kwargs):
            stream = kwargs.get("stream", False)
            with tracer.start_as_current_span(
                f"openai.{original_acreate.__qualname__}"
            ) as span:
                response = await original_acreate(*args, **kwargs)
                if stream:

                    async def stream_wrapper():
                        first_chunk = True
                        async for resp in response:
                            if first_chunk:
                                self._handle_attributes(span, kwargs, resp)
                                first_chunk = False
                            yield resp

                    return stream_wrapper()
                else:
                    self._handle_attributes(span, kwargs, response)
                    return response  # type: ignore

        return wrapper
