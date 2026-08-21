import uuid
from litestar import Controller
from litestar import get
from litestar import post
from litestar import Request

from quiz_examples.code_snippet.background.courses import CoursesWorker
from quiz_examples.code_snippet.core.courses import check_user_have_access_to_course
from quiz_examples.code_snippet.core.repository import MockedRepository
from quiz_examples.code_snippet.core.user import extract_user_from_cookies
from quiz_examples.code_snippet.models.course import CourseModel


class CoursesController(Controller):
    path = "/courses/{course_id:uuid}"

    @get(path="/")
    async def get_course(self, request: Request, course_id: uuid.UUID) -> CourseModel:
        user = await extract_user_from_cookies(request=request, repository=request.app.state.repository)
        course = await request.app.state.repository.get_course(course_id)
        access = check_user_have_access_to_course(
            user=user,
            course=course
        )
        if access:
            return course
        raise PermissionError("User doesn't have access to this course")

    @post(path="/apply_to_course")  # <-- here
    async def apply_to_course(self, request: Request, course_id: uuid.UUID, courses_worker: CoursesWorker, db_repository: MockedRepository) -> None:
        user = await extract_user_from_cookies(request=request, repository=db_repository)

        _application = await courses_worker.apply_to_course(user_id=user.id, course_id=course_id)

        return None


