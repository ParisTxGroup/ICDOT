import json

import pytest
import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import RequestFactory

from icdot.histomx.views import histomx_report_request_view
from icdot.users.models import User

pytestmark = pytest.mark.django_db


def _build_json_for_schema(schema):
    # This could probably be achieved by something like
    # hypothesis-jsonschema, feel free to integrate that but it might
    # be a bit tricky since the `@given()` decorater might not work
    # since the schema isn't available at that time.

    default_providers = {
        "string": "test-string",
        "number": 123,
    }

    result = {}

    assert schema["type"] == "object"
    for key, value in schema["keys"].items():
        if "default" in value:
            result[key] = value["default"]
        else:
            result[key] = default_providers[value["type"]]

    return result


def test_histomx_request(requests_mock, user: User, rf: RequestFactory):

    permission = Permission.objects.get(codename="add_histomxreportrequest")
    user.user_permissions.add(permission)

    # This is mocking the request to the actual histomx server.
    expected_response = {"foo": "bar"}
    requests_mock.post(
        settings.HISTOMX_SERVICE_URL + "histomx_report/html",
        json=expected_response,
        headers={"content-type": "application/json"},
    )

    # This is the request to django, which should in turn trigger the above.
    request = rf.post(
        "/histomx/",
        data={
            "RCC_file": SimpleUploadedFile("file", b"data"),
            "template": "DEFAULT",
            "rna_metadata": json.dumps(
                _build_json_for_schema(
                    histomx_report_request_view.view_class.model.rna_metadata.field.schema
                )
            ),
            "patient_metadata": json.dumps(
                _build_json_for_schema(
                    histomx_report_request_view.view_class.model.patient_metadata.field.schema
                )
            ),
        },
        format="multipart",
    )
    request.user = user
    response = histomx_report_request_view(request)

    assert response.status_code == 200
    # Without the next line, we won't notice until trying to parse HTML as JSON.
    # This is because Django returns a 200 on POSTs with invalid forms...
    assert (
        isinstance(response, HttpResponse) or not response.context_data["form"].errors
    )
    assert json.loads(response.content) == expected_response


def test_histomx_request_exception(requests_mock, user: User, rf: RequestFactory):

    permission = Permission.objects.get(codename="add_histomxreportrequest")
    user.user_permissions.add(permission)

    # This is mocking the request to the actual histomx server.
    requests_mock.post(
        settings.HISTOMX_SERVICE_URL + "histomx_report/html",
        exc=requests.exceptions.ConnectTimeout,
    )

    # This is the request to django, which should in turn trigger the above.
    request = rf.post(
        "/histomx/",
        data={
            "RCC_file": SimpleUploadedFile("file", b"data"),
            "template": "DEFAULT",
            "rna_metadata": json.dumps(
                _build_json_for_schema(
                    histomx_report_request_view.view_class.model.rna_metadata.field.schema
                )
            ),
            "patient_metadata": json.dumps(
                _build_json_for_schema(
                    histomx_report_request_view.view_class.model.patient_metadata.field.schema
                )
            ),
        },
        format="multipart",
    )
    request.user = user
    response = histomx_report_request_view(request)

    assert response.status_code == 500


def test_histomx_request_permission(requests_mock, user: User, rf: RequestFactory):

    request = rf.get("/histomx/")
    request.user = user

    with pytest.raises(PermissionDenied):
        histomx_report_request_view(request)

    request = rf.post(
        "/histomx/",
        data={
            "RCC_file": SimpleUploadedFile("file", b"data"),
        },
        format="multipart",
    )
    request.user = user

    with pytest.raises(PermissionDenied):
        histomx_report_request_view(request)
