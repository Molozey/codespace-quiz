import uuid

from litestar import Controller, get

from quiz_examples.code_snippet.core.repository import MockedRepository
from quiz_examples.code_snippet.models import UserModel


class UserController(Controller):
    path = "/user"

    @get(path="/{user_id:uuid}")
    async def get(
        self, user_id: uuid.UUID, db_repository: MockedRepository
    ) -> UserModel:
        return await db_repository.get_user(user_id=user_id)
