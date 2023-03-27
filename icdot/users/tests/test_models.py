import django_scopes.exceptions
import pytest
import tablib
from django.db import connection, models
from import_export import resources

from icdot.users.models import User, UserRecordingModel, UserScopedModel
from icdot.users.tests.factories import UserFactory
from icdot.utils.threadlocal import current_user

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


def test_user_scoped_model_work_with_resources():
    user1, user2 = UserFactory(), UserFactory()

    class TestModel(UserScopedModel):
        id_field_one = models.CharField(max_length=255)
        id_field_two = models.CharField(max_length=255)
        data = models.CharField(max_length=255)

    # Create the schema for our test model
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestModel)

    class TestModelResource(resources.ModelResource):
        class Meta:
            model = TestModel
            exclude = ["id"]
            import_id_fields = ["id_field_one", "id_field_two"]

    # Now make some data as different users.

    DATA = (
        ("foo", "bar", "data"),
        ("spam", "eggs", "data"),
    )

    for user in (user1, user2):
        with current_user(user):
            with django_scopes.scope(user=user):
                for one, two, data in DATA:
                    TestModel.objects.get_or_create(
                        id_field_one=one, id_field_two=two, data=data
                    )

    with django_scopes.scopes_disabled():
        assert TestModel.objects.count() == 4

    dataset = tablib.Dataset(headers=("id_field_one", "id_field_two", "data"))
    dataset.append(("foo", "bar", "new data"))

    with current_user(user1):
        with pytest.raises(django_scopes.exceptions.ScopeError):
            TestModelResource().import_data(dataset, raise_errors=True, dry_run=False)
        with django_scopes.scope(user=user1):
            TestModelResource().import_data(dataset, raise_errors=True, dry_run=False)

    with django_scopes.scopes_disabled():
        assert TestModel.objects.count() == 4
        edited = TestModel.objects.get(created_by=user1, data="new data")
        edited.delete()
