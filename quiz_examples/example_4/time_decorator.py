import asyncio

from pydantic import BaseModel

from quiz_examples.example_4.receiver import RECEIVERS_MAP

_LONG_WAIT = 2
_SMALL_WAIT = 0.5


class FunctionResult(BaseModel):
    name: str
    long_flag: bool

    def __str__(self):
        return f"Function [{self.name}] finished with {self.long_flag=}"


def time_decorator(method: str):
    pass


async def send_feedback(method: str, elapsed_time: float) -> None:
    result = await RECEIVERS_MAP[method].receive_message(
        message={"elapsed_time": elapsed_time, "params": None}
    )
    if not result.status:
        print(f"Error: {result.reason}")


async def non_stable_function(_index: int, name: str) -> FunctionResult:
    _long_flag = False
    if (_index % 5) < 3:
        _long_flag = True
        await asyncio.sleep(_LONG_WAIT)
        # We want to automate await send_feedback(method="3", elapsed_time=_LONG_WAIT) here
    else:
        await asyncio.sleep(_SMALL_WAIT)
    _result = FunctionResult(name=name, long_flag=_long_flag)
    print(_result)
    return _result


async def main():
    tasks = [non_stable_function(_index=idx, name=f"Task:{idx}") for idx in range(10)]
    _ = await asyncio.gather(*tasks)


if __name__ == "__main__":
    # two methods: ["1", "2", "3"]
    asyncio.run(main())
