import asyncio
import uuid


class MockedPublisher:
    async def publish_course_application(self, user_id: uuid.UUID, course_id: uuid.UUID):
        _ = self, user_id, course_id
        await asyncio.sleep(2)
        pass
