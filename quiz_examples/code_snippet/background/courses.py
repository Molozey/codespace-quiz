import asyncio
import uuid
from queue import Empty, Queue

from quiz_examples.code_snippet.core.publisher import MockedPublisher
from quiz_examples.code_snippet.core.repository import MockedRepository


class CoursesWorker:
    def __init__(self, db_repository: MockedRepository, publisher: MockedPublisher):
        self._queue: Queue[tuple[uuid.UUID, uuid.UUID]] = Queue(maxsize=64)
        self._processed_tasks: set[tuple[uuid.UUID, uuid.UUID]] = set()
        self._db_repository = db_repository
        self._publisher = publisher

    async def apply_to_course(self, user_id: uuid.UUID, course_id: uuid.UUID):
        self._queue.put((user_id, course_id))
        print(f"Now queue is: {self._queue.qsize()}")

    async def run(self):
        while True:
            # print("Running loop ...")
            try:
                obj = self._queue.get(block=False, timeout=0.5)
                user_id, course_id = obj
                print(">" * 10, f"Got task ({user_id}, {course_id}")
            except Empty:
                await asyncio.sleep(0.5)
                continue
            if (user_id, course_id) in self._processed_tasks:
                print(f"Task ({user_id}, {course_id}) already processed")
                return

            await self.process_course_application(user_id, course_id)
            await asyncio.sleep(10)

    async def process_course_application(
        self, user_id: uuid.UUID, course_id: uuid.UUID
    ):
        print("Start processing course application ...")
        _ = await self._db_repository.apply_user_to_course(user_id, course_id)
        _ = await self._publisher.publish_course_application(user_id, course_id)
        print("Course application processed")
