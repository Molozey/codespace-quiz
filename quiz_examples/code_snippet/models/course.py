import random
import uuid

from pydantic import BaseModel


class CourseModel(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    public: bool = False

    @staticmethod
    def cpu_bound_operation() -> int:
        _ = 0
        for i in range(100_000 + random.randint(10, 20)):
            _ += i
        return _ % 2
