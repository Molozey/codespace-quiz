import uuid

from litestar import Request

from quiz_examples.code_snippet.core.repository import MockedRepository
from quiz_examples.code_snippet.models import UserModel


async def extract_user_from_cookies(
    request: Request, repository: MockedRepository
) -> UserModel:
    user_id = request.cookies.get("user_id") or "1af22490-3e94-483d-b2d5-c7cd4832bbbc"
    # Please note that this is just a dummy check to simplify the example
    return await repository.get_user(user_id=uuid.UUID(user_id))
