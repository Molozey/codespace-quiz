import asyncio
from abc import ABC, abstractmethod

from limits import RateLimitItemPerSecond
from limits.aio.storage.memory import MemoryStorage
from limits.aio.strategies import MovingWindowRateLimiter

from quiz_examples.example_4.models import ReceiverResult


class AbstractReceiver(ABC):
    @abstractmethod
    async def receive_message(self, message: dict) -> ReceiverResult:
        pass


class AlwaysGoodReceiver(AbstractReceiver):
    async def receive_message(self, message: dict) -> ReceiverResult:
        return ReceiverResult(status=1, reason=None)


class LimitedReceiver(AbstractReceiver):
    def __init__(self):
        self._limiter = MovingWindowRateLimiter(storage=MemoryStorage())
        self._limit_window = RateLimitItemPerSecond(amount=1)

    async def receive_message(self, message: dict) -> ReceiverResult:
        _hit = await self._limiter.hit(self._limit_window, "test_space", "foo")
        if _hit:
            return ReceiverResult(status=1, reason=None)
        return ReceiverResult(status=0, reason="Rate limit exceeded")


class LimitedConnectionsReceiver(AbstractReceiver):
    def __init__(self):
        self._number_of_connections = 0
        self._max_number_of_connections = 2

    async def receive_message(self, message: dict) -> ReceiverResult:
        self._number_of_connections += 1
        try:
            await asyncio.sleep(1)
            if self._number_of_connections > self._max_number_of_connections:
                return ReceiverResult(status=0, reason="Too many connections")
            else:
                return ReceiverResult(status=1, reason=None)
        finally:
            self._number_of_connections -= 1


RECEIVERS_MAP = {
    "1": AlwaysGoodReceiver(),
    "2": LimitedReceiver(),
    "3": LimitedConnectionsReceiver(),
}
