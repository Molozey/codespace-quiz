import uuid
from litestar import Controller
from litestar import get
from litestar import post
from litestar import Request
from pydantic import BaseModel

from quiz_examples.code_snippet.background.courses import CoursesWorker
from quiz_examples.code_snippet.core.courses import check_user_have_access_to_course
from quiz_examples.code_snippet.core.repository import MockedRepository
from quiz_examples.code_snippet.core.user import extract_user_from_cookies
from quiz_examples.code_snippet.models.course import CourseModel

class AllCoursesModel(BaseModel):
    courses: list[CourseModel]

    total: int
    num_public: int
    num_private: int

    trending: int

class CoursesController(Controller):
    path = "/courses"

    @get(path="/{course_id:uuid}/")
    async def get_course(self, request: Request, course_id: uuid.UUID, db_repository: MockedRepository) -> CourseModel:
        user = await extract_user_from_cookies(request=request, repository=db_repository)
        course = await db_repository.get_course(course_id)
        access = check_user_have_access_to_course(
            user=user,
            course=course
        )
        if access:
            return course
        raise PermissionError("User doesn't have access to this course")

    @post(path="/{course_id:uuid}/apply_to_course")  # <-- here
    async def apply_to_course(self, request: Request, course_id: uuid.UUID, courses_worker: CoursesWorker, db_repository: MockedRepository) -> None:
        user = await extract_user_from_cookies(request=request, repository=db_repository)

        _application = await courses_worker.apply_to_course(user_id=user.id, course_id=course_id)

        return None


    @get(path="/all-courses")
    async def get_all_courses(self, repository: MockedRepository) -> AllCoursesModel:
        _private = 0
        _public = 0
        _trending = 0

        _all_courses = await repository.get_all_courses()
        for course in _all_courses:
            if course.public:
                _public += 1
            else:
                _private += 1

            if course.cpu_bound_operation():
                _trending += 1

        return AllCoursesModel(
            courses=_all_courses,
            total=len(_all_courses),
            num_public=_public,
            num_private=_private,
            trending=_trending
        )

