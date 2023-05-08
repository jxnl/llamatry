from opentelemetry import trace
from typing import Callable, Union

import inspect


def simple_args_to_dict(func, *args, **kwargs):
    """
    Return a dictionary of the arguments
    Does not include default arguments or keyword arguments that are not strings
    This helps avoid sending too much data to the OpenTelemetry backend.
    """
    arg_dict = {}

    # Get the names of the positional arguments
    signature = inspect.signature(func)
    param_names = list(signature.parameters.keys())

    # Populate the dictionary with the positional arguments
    for ii, arg in enumerate(args):
        if isinstance(arg, (str, bool, float, int)):
            arg_name = param_names[ii]
            arg_dict[arg_name] = arg

    # Populate the dictionary with the keyword arguments
    for key, value in kwargs.items():
        if isinstance(arg, (str, bool, float, int)):
            arg_dict[key] = value

    return arg_dict


def tracer(*args: Union[str, Callable]) -> Union[Callable, None]:
    def _decorator(func: Callable, span_name: str) -> Callable:
        def wrapped(*args, **kwargs):
            tracer = trace.get_tracer("llamatry")

            with tracer.start_as_current_span(span_name) as span:
                result = func(*args, **kwargs)

                arg_dict = simple_args_to_dict(func, *args, **kwargs)
                for key, value in arg_dict.items():
                    span.set_attribute(key, value)

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

    @classmethod
    def get_current_span(self):
        return trace.get_current_span()
