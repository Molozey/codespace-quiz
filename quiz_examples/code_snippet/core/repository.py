import asyncio
import uuid

from quiz_examples.code_snippet.models import UserModel
from quiz_examples.code_snippet.models.course import CourseModel
from faker import Faker
from functools import lru_cache

class MockedRepository:
    def __init__(self):
        self._in_memory_users: dict[str, UserModel] = {}
        self._in_memory_user_credits: dict[uuid.UUID, str] = {}

    @staticmethod
    async def _make_db_request():
        await asyncio.sleep(0.5)

    async def get_course(self, course_id: uuid.UUID) -> CourseModel:
        await self._make_db_request()
        return CourseModel(
            id=course_id,
            name="Course name",
            description="Course description"
        )

    async def get_user(self, user_id: uuid.UUID) -> UserModel:
        await self._make_db_request()
        # Please note that this is just a dummy check to simplify the example
        user = UserModel(
            id=user_id,
            email=f"dummy-{user_id}@example.com"
        )
        return user

    async def apply_user_to_course(self, user_id: uuid.UUID, course_id: uuid.UUID):
        pass

    async def register_user(self, email: str, password: str) -> UserModel:
        if email in self._in_memory_users:
            raise ValueError("User with this email already exists")
        user = UserModel(
            id=uuid.uuid4(),
            email=email
        )
        self._in_memory_users[email] = user
        self._in_memory_user_credits[user.id] = password
        return user

    async def login_user(self, email: str, password: str) -> UserModel:
        if email not in self._in_memory_users:
            raise ValueError("User with this email doesn't exist")
        user = self._in_memory_users[email]
        if self._in_memory_user_credits[user.id] != password:
            raise ValueError("Wrong password")
        return user

    # @lru_cache
    async def get_all_courses(self) -> list[CourseModel]:
        pass
