import asyncio
from asyncio.queues import Queue

QUEUE = Queue(maxsize=10)

class ProcessorBuffer:
    def __init__(self):
        self._queue = QUEUE

    async def run(self):
        while True:
            _id = await self._queue.get()
            print(f"Received {_id} from queue")
            await asyncio.sleep(1)


async def put_task(task_id: int):
    await QUEUE.put(task_id)
    print(f"Put task [{task_id}] to queue")

async def main():
    _processor = ProcessorBuffer()
    loop = asyncio.get_event_loop()
    loop.create_task(_processor.run())
    tasks = [
        asyncio.create_task(put_task(task_id=i))
        for i in range(100)
    ]

    # await asyncio.sleep(100)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())