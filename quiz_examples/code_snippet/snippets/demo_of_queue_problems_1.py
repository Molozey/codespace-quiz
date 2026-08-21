import asyncio
from queue import Queue

QUEUE = Queue(maxsize=10)

class ProcessorBuffer:
    def __init__(self):
        self._queue = QUEUE

    async def run(self):
        while True:
            _id = self._queue.get()
            print(f"Received {_id} from queue")


async def put_task(task_id: int):
    QUEUE.put(task_id)
    print(f"Put task [{task_id}] to queue")

async def main():
    _processor = ProcessorBuffer()
    loop = asyncio.get_event_loop()
    loop.create_task(_processor.run())
    loop.create_task(put_task(task_id=1))

    await asyncio.sleep(10)
if __name__ == "__main__":
    asyncio.run(main())