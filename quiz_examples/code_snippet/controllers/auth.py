import litestar
from litestar import Controller, get, post
from pydantic import BaseModel

from quiz_examples.code_snippet.core.repository import MockedRepository
from quiz_examples.code_snippet.models import UserModel


class RegisterData(BaseModel):
    email: str
    password: str


class AuthController(Controller):
    path = "/auth"

    @post(path="/login")
    async def login(
        self, data: RegisterData, repository: MockedRepository
    ) -> UserModel:
        user = await repository.login_user(email=data.email, password=data.password)
        return user

    @post(path="/register")
    async def register(
        self, data: RegisterData, repository: MockedRepository
    ) -> UserModel:
        user = await repository.register_user(email=data.email, password=data.password)
        return user

    @post(path="/login/google")
    async def login_with_google(self) -> None:
        raise NotImplementedError

    @post(path="/register/google")
    async def register_with_google(self) -> None:
        raise NotImplementedError

    @post(path="/login/github")
    async def login_with_github(self) -> None:
        raise NotImplementedError

    @post(path="/register/github")
    async def register_with_github(self) -> None:
        raise NotImplementedError

    @post(path="/login/facebook")
    async def login_with_facebook(self) -> None:
        raise NotImplementedError

    @post(path="/register/facebook")
    async def register_with_facebook(self) -> None:
        raise NotImplementedError

    @get(path="/current-session")
    async def get_current_session(self, request: litestar.Request) -> dict:
        _cookie = request.cookies.get("session_id")
        return {"session_id": _cookie}
