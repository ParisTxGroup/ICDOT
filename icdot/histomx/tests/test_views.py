import json

import pytest
import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory

from icdot.histomx.views import histomx_report_request_view
from icdot.users.models import User

pytestmark = pytest.mark.django_db


def test_histomx_request(requests_mock, user: User, rf: RequestFactory):

    permission = Permission.objects.get(codename="add_histomxreportrequest")
    user.user_permissions.add(permission)

    payload = {"foo": "bar"}

    requests_mock.post(
        settings.HISTOMX_SERVICE_URL + "histomx_report/html",
        json=payload,
        headers={"content-type": "application/json"},
    )

    request = rf.post(
        "/histomx/",
        data={
            "RCC_file": SimpleUploadedFile("file", b"data"),
        },
        format="multipart",
    )
    request.user = user
    response = histomx_report_request_view(request)

    assert response.status_code == 200
    assert json.loads(response.content) == payload


def test_histomx_request_exception(requests_mock, user: User, rf: RequestFactory):

    permission = Permission.objects.get(codename="add_histomxreportrequest")
    user.user_permissions.add(permission)

    requests_mock.post(
        settings.HISTOMX_SERVICE_URL + "histomx_report/html",
        exc=requests.exceptions.ConnectTimeout,
    )

    request = rf.post(
        "/histomx/",
        data={
            "RCC_file": SimpleUploadedFile("file", b"data"),
        },
        format="multipart",
    )
    request.user = user
    response = histomx_report_request_view(request)

    assert response.status_code == 500


def test_histomx_request_permission(requests_mock, user: User, rf: RequestFactory):

    payload = {"foo": "bar"}

    requests_mock.post(
        settings.HISTOMX_SERVICE_URL + "histomx_report/html",
        json=payload,
        headers={"content-type": "application/json"},
    )

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
