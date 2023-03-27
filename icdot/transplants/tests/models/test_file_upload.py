import pytest
from django.core import exceptions
from django.db import connection, models
from model_bakery import baker

from icdot.transplants.models import FileUpload, SequencingData
from icdot.transplants.models.file_upload import TrackFileUploadModel
from icdot.users.models import UserScopedModel
from icdot.utils.middleware import current_user_and_scope

pytestmark = pytest.mark.django_db


def test_ref_in_name():
    file_upload = baker.prepare(FileUpload, file_ref="ref-one", file_path="path")
    assert "ref-one" in str(file_upload)


def test_upload_before_model(user):
    with current_user_and_scope(user=user):
        baker.make(FileUpload, file_ref="ref-one", file_path="path")
        sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        assert sequencing_data.file_path == "path"


def test_upload_after_model(user):
    with current_user_and_scope(user=user):
        sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        assert not sequencing_data.file_path
        baker.make(FileUpload, file_ref="ref-one", file_path="path")
        sequencing_data.refresh_from_db()
        assert sequencing_data.file_path == "path"


def test_upload_ref_change_sets_model_path(user):
    with current_user_and_scope(user=user):
        file_upload = baker.make(FileUpload, file_ref="ref-one", file_path="path")
        sequencing_data = baker.make(SequencingData, file_ref="ref-two")
        file_upload.file_ref = "ref-two"
        file_upload.save()
        sequencing_data.refresh_from_db()
        assert sequencing_data.file_path == "path"


def test_upload_ref_change_keeps_model_path(user):
    with current_user_and_scope(user=user):
        file_upload = baker.make(FileUpload, file_ref="ref-one", file_path="path")
        sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        file_upload.file_ref = "ref-two"
        file_upload.save()
        sequencing_data.refresh_from_db()
        assert sequencing_data.file_path == "path"


def test_upload_duplicate_ref_change_sets_model_path(user):
    with current_user_and_scope(user=user):
        sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        baker.make(FileUpload, file_ref="ref-one", file_path="path_one")
        baker.make(FileUpload, file_ref="ref-one", file_path="path_two")
        sequencing_data.refresh_from_db()
        assert sequencing_data.file_path == "path_two"


def test_upload_deleted(user):
    with current_user_and_scope(user=user):
        file_upload = baker.make(FileUpload, file_ref="ref-one", file_path="path")
        sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        file_upload.delete()
        sequencing_data.refresh_from_db()
        assert sequencing_data.file_path == "path"


def test_model_ref_changes(user):
    with current_user_and_scope(user=user):
        baker.make(FileUpload, file_ref="ref-one", file_path="path_one")
        baker.make(FileUpload, file_ref="ref-two", file_path="path_two")
        sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        assert sequencing_data.file_path == "path_one"
        sequencing_data.file_ref = "ref-two"
        sequencing_data.save()
        assert sequencing_data.file_path == "path_two"


def test_model_ref_ambigous(user):
    with current_user_and_scope(user=user):
        baker.make(FileUpload, file_ref="ref-one", file_path="path_one")
        baker.make(FileUpload, file_ref="ref-one", file_path="path_two")
        with pytest.raises(FileUpload.MultipleObjectsReturned):
            sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        with pytest.raises(exceptions.ValidationError) as e:
            sequencing_data = baker.prepare(SequencingData, file_ref="ref-one")
            sequencing_data.clean()
        assert any("ambigious" in v.message for v in e.value.error_dict["file_ref"])


def test_multiple_refs(user):
    class TrackingMultipleFiles(UserScopedModel, TrackFileUploadModel):
        ref_one = models.CharField(max_length=256, blank=True)
        ref_two = models.CharField(max_length=256, blank=True)
        path_one = models.FileField(null=True, editable=False)
        path_two = models.FileField(null=True, editable=False)

        TRACK_FILE_UPLOAD = {"ref_one": "path_one", "ref_two": "path_two"}

    # Create the schema for our test model
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TrackingMultipleFiles)

    with current_user_and_scope(user=user):
        upload_one = baker.make(FileUpload, file_ref="ref-one", file_path="path_one")
        upload_two = baker.make(FileUpload, file_ref="ref-two", file_path="path_two")
        data = baker.make(TrackingMultipleFiles, ref_one="ref-one", ref_two="ref-two")
        assert data.path_one == "path_one"
        assert data.path_two == "path_two"
        upload_one.file_path = "path_one_update"
        upload_one.save()
        upload_two.file_path = "path_two_update"
        upload_two.save()
        data.refresh_from_db()
        assert data.path_one == "path_one_update"
        assert data.path_two == "path_two_update"

    # Cleanup after ourselves, we don't want to keep listening to signals.
    TrackingMultipleFiles.disconnect_signals()


def test_untouched_ref_does_not_cause_query(user, django_assert_num_queries):
    with current_user_and_scope(user=user):
        baker.make(FileUpload, file_ref="ref-one", file_path="path-one")
        baker.make(FileUpload, file_ref="ref-two", file_path="path-two")
        sequencing_data = baker.make(SequencingData, file_ref="ref-one")
        assert sequencing_data.file_path == "path-one"
        with django_assert_num_queries(2):
            sequencing_data.file_ref = "ref-two"
            sequencing_data.save()
            assert sequencing_data.file_path == "path-two"
        with django_assert_num_queries(1):
            sequencing_data.file_ref = "ref-two"
            sequencing_data.save()
            assert sequencing_data.file_path == "path-two"
