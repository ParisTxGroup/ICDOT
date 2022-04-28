from django.urls import path

from icdot.histomx.views import histomx_report_request_view

app_name = "histomx"
urlpatterns = [
    path("", histomx_report_request_view, name="histomx_report_view"),
]
