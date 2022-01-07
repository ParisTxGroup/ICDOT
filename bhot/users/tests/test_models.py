import django_scopes.exceptions
import pytest
from django.db import connection

from bhot.users.models import User, UserRecordingModel, UserScopedModel
from bhot.users.tests.factories import UserFactory
from bhot.utils.threadlocal import current_user

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_recording_model_updates_created_and_modified():

    user1, user2 = UserFactory(), UserFactory()

    class TestUserRecordingModel(UserRecordingModel):
        pass

    # Create the schema for our test model
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestUserRecordingModel)

    test = TestUserRecordingModel()

    with current_user(user1):
        test.save()

    assert test.created_by == user1
    assert test.modified_by == user1

    with current_user(user2):
        test.save()

    assert test.created_by == user1
    assert test.modified_by == user2


def test_user_scoped_model_limits_queries():

    user1, user2 = UserFactory(), UserFactory()

    class TestUserScopedModel(UserScopedModel):
        pass

    # Create the schema for our test model
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestUserScopedModel)

    with current_user(user1):
        test1 = TestUserScopedModel()
        test1.save()

    with current_user(user2):
        test2 = TestUserScopedModel()
        test2.save()

    with pytest.raises(django_scopes.exceptions.ScopeError):
        assert TestUserScopedModel.objects.count() == 2

    with django_scopes.scope(user=None):
        assert TestUserScopedModel.objects.count() == 2

    with django_scopes.scope(user=user1):
        assert TestUserScopedModel.objects.count() == 1
        assert TestUserScopedModel.objects.first() == test1

    with django_scopes.scope(user=user2):
        assert TestUserScopedModel.objects.count() == 1
        assert TestUserScopedModel.objects.first() == test2
