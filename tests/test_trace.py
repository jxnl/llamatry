import pytest
import asyncio
from llamatry import Trace


def test_decorator():
    @Trace.trace
    def add(a, b):
        return a + b

    assert add(1, 2) == 3


def test_decorator_with_name():
    @Trace.trace("add")
    def add(a, b):
        return a + b

    assert add(1, 2) == 3


@pytest.mark.asyncio
async def test_decorator_async():
    @Trace.trace
    async def add(a, b):
        return a + b

    assert await add(1, 2) == 3


@pytest.mark.asyncio
async def test_decorator_async_with_name():
    @Trace.trace("add")
    async def add(a, b):
        return a + b

    assert await add(1, 2) == 3


def test_decorator_with_tracer():
    with Trace.span("add") as span:
        assert 1 + 2 == 3


@pytest.mark.asyncio
async def test_decorator_async_with_tracer():
    with Trace.span("add") as span:
        await asyncio.sleep(1)
