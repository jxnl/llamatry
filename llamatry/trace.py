from opentelemetry import trace
from typing import Callable, Union


def tracer(*args: Union[str, Callable]) -> Union[Callable, None]:
    def _decorator(func: Callable, span_name: str) -> Callable:
        def wrapped(*args, **kwargs):
            tracer = trace.get_tracer("llamatry")

            with tracer.start_as_current_span(span_name):
                result = func(*args, **kwargs)

            return result

        return wrapped

    if len(args) == 1 and isinstance(args[0], str):
        # If the argument is a string, use the string as the span name
        # Example usage: @trace_decorator("name")
        def _partial(func: Callable) -> Callable:
            return _decorator(func, args[0])

        return _partial
    elif len(args) == 1 and callable(args[0]):
        # If the argument is a function, use the function name as the span name
        # Example usage: @trace_decorator
        return _decorator(args[0], args[0].__name__)
    else:
        raise ValueError("Invalid arguments for trace_decorator")


class Trace:
    @classmethod
    def trace(cls, *args, **kwargs):
        return tracer(*args, **kwargs)

    @classmethod
    def span(self, *args, **kwargs):
        return trace.get_tracer("llamatry").start_as_current_span(*args, **kwargs)
