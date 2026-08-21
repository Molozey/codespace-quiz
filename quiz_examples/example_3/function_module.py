import datetime
import uuid

from pydantic import BaseModel


class Object(BaseModel):
    public: bool


class RegistrationDetails(BaseModel):
    registered_at: datetime.datetime


class BanReason(BaseModel):
    reason: str
    moderator_id: uuid.UUID


class RestrictionDetails(BaseModel):
    ban_reason: BanReason


class User(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    registration_details: RegistrationDetails | None
    restriction_details: RestrictionDetails | None


def check_object_access(user: User, obj: Object) -> tuple[bool, str | None]:
    if user.restriction_details:
        return False, user.restriction_details.ban_reason.reason
    if obj.public:
        return True, None
    if not user.registration_details:
        return False, "Object is private"

    return True, None
