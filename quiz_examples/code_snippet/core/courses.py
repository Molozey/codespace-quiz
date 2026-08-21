import uuid

from quiz_examples.code_snippet.core.repository import MockedRepository
from quiz_examples.code_snippet.models import UserModel
from quiz_examples.code_snippet.models.course import CourseModel

async def receive_course_info(course_id: uuid.UUID, repository: MockedRepository) -> CourseModel:
    course = await repository.get_course(course_id)
    return course

def check_user_have_access_to_course(user: UserModel, course: CourseModel):
    _ = user, course
    # Please note that this is just a dummy check to simplify the example
    return True