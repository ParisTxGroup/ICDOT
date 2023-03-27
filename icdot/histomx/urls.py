from django.urls import path

from icdot.histomx.views import histomx_report_request_view, histomx_timeout_view

app_name = "histomx"
urlpatterns = [
    path("", histomx_report_request_view, name="histomx_report_view"),
    path("timeout/<int:timeout>/", histomx_timeout_view, name="histomx_timeout_view"),
]
