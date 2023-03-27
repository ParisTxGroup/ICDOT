import django_scopes
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from icdot.transplants.models import FileUpload, FileUploadBatch

pytestmark = pytest.mark.django_db


def test_save_related(admin_client):
    with django_scopes.scopes_disabled():
        FileUpload.objects.all().delete()
        FileUploadBatch.objects.all().delete()

    url = reverse("admin:transplants_fileuploadbatch_add")
    response = admin_client.get(url)
    assert response.status_code == 200

    response = admin_client.post(
        url,
        data={
            "files-TOTAL_FORMS": 0,
            "files-INITIAL_FORMS": 0,
            "files-MAX)NUM_FORMS": 0,
            "files": [SimpleUploadedFile(f"name_{i}", b"content") for i in range(5)],
        },
    )

    assert response.status_code == 302
    with django_scopes.scopes_disabled():
        assert FileUploadBatch.objects.all().count() == 1
        assert FileUpload.objects.all().count() == 5
