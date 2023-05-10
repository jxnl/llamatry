import pytest
import asyncio
from llamatry import tracer


def test_decorator():
    @tracer.wrap
    def add(a, b):
        return a + b

    assert add(1, 2) == 3


def test_decorator_with_name():
    @tracer.wrap("add")
    def add(a, b):
        return a + b

    assert add(1, 2) == 3


@pytest.mark.asyncio
async def test_decorator_async():
    @tracer.wrap
    async def add(a, b):
        return a + b

    assert await add(1, 2) == 3


@pytest.mark.asyncio
async def test_decorator_async_with_name():
    @tracer.wrap("add")
    async def add(a, b):
        return a + b

    assert await add(1, 2) == 3


def test_decorator_with_tracer():
    with tracer.trace("add") as span:
        assert 1 + 2 == 3


@pytest.mark.asyncio
async def test_decorator_async_with_tracer():
    with tracer.trace("add") as span:
        await asyncio.sleep(1)
