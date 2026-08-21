import uuid

from pydantic import BaseModel

class CourseModel(BaseModel):
    id: uuid.UUID
    name: str
    description: str
