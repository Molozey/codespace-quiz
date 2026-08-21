from unittest.mock import Mock

from litestar import Controller
from litestar import get, post

from quiz_examples.code_snippet.core.repository import MockedRepository
from pydantic import BaseModel

from quiz_examples.code_snippet.models import UserModel


class RegisterData(BaseModel):
    email: str
    password: str

class AuthController(Controller):
    path = "/auth"

    @post(path="/login")
    async def login(self, data: RegisterData, repository: MockedRepository) -> UserModel:
        user = await repository.login_user(email=data.email, password=data.password)
        return user

    @post(path="/register")
    async def register(self, data: RegisterData, repository: MockedRepository) -> UserModel:
        user = await repository.register_user(email=data.email, password=data.password)
        return user

    @post(path="/login/google")
    async def login_with_google(self):
        pass

    @post(path="/register/google")
    async def register_with_google(self):
        pass

    @post(path="/login/github")
    async def login_with_github(self):
        pass

    @post(path="/register/github")
    async def register_with_github(self):
        pass


    @post(path="/login/facebook")
    async def login_with_facebook(self):
        pass

    @post(path="/register/facebook")
    async def register_with_facebook(self):
        pass