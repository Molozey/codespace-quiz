import uuid

import pytest
from faker import Faker

from quiz_examples.pytest_example_2.function_module import (
    BanReason,
    Object,
    RegistrationDetails,
    RestrictionDetails,
    User,
    check_object_access,
)


@pytest.fixture(autouse=True)
def global_faker() -> Faker:
    return Faker(locale="ru")


def test_registered_user_access(global_faker):
    _user = User(
        id=uuid.uuid4(),
        email=global_faker.email(),
        name=global_faker.name(),
        registration_details=RegistrationDetails(
            registered_at=global_faker.date_time()
        ),
        restriction_details=None,
    )
    _obj = Object(public=False)

    status, reason = check_object_access(user=_user, obj=_obj)
    assert status
    assert not reason


def test_non_registered_user_access(global_faker):
    _user = User(
        id=uuid.uuid4(),
        email=global_faker.email(),
        name=global_faker.name(),
        registration_details=None,
        restriction_details=None,
    )
    _obj = Object(public=True)

    status, reason = check_object_access(user=_user, obj=_obj)
    assert status
    assert not reason


def test_banned_user_access(global_faker):
    _user = User(
        id=uuid.uuid4(),
        email=global_faker.email(),
        name=global_faker.name(),
        registration_details=RegistrationDetails(
            registered_at=global_faker.date_time()
        ),
        restriction_details=RestrictionDetails(
            ban_reason=BanReason(reason="spam", moderator_id=uuid.uuid4())
        ),
    )
    _obj = Object(public=True)

    status, reason = check_object_access(user=_user, obj=_obj)
    assert not status
    assert reason
