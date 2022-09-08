import requests
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from icdot.histomx.models import HistomxReportRequest


class HistomxReportRequestFormView(PermissionRequiredMixin, CreateView):
    permission_required = "histomx.add_histomxreportrequest"
    template_name = "histomx/request_histomx_report.html"
    model = HistomxReportRequest
    fields = ["RCC_file", "render_pdf"]

    def form_valid(self, form):
        """Overwrite default database behavior and render the result."""

        # This model should not be saved to the database,
        # because we don't need to remember it and because it is not managed.

        histomx_report_request = form.save(commit=False)

        try:
            content, content_type = histomx_report_request.get_report()
        except requests.exceptions.RequestException as e:
            return render(
                self.request,
                "histomx/histomx_not_available.html",
                dict(
                    attempted_url=e.request.url if e.request else None,
                ),
                status=500,
            )
        except ValueError:
            form.add_error(
                "RCC_file",
                _(
                    "We're having trouble generating a report. Was that a valid RCC file?"
                ),
            )
            return super().form_invalid(form)

        return HttpResponse(content, content_type=content_type)


if HistomxReportRequest.PROBABLY_NOT_AVAILABLE:
    histomx_report_request_view = TemplateView.as_view(
        template_name="histomx/histomx_not_available.html",
    )
else:
    histomx_report_request_view = HistomxReportRequestFormView.as_view()
