from urllib.parse import urljoin

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField


class HistomxReportRequest(models.Model):

    PROBABLY_NOT_AVAILABLE = settings.HISTOMX_SERVICE_URL is None

    class Meta:
        managed = False  # No database table creation or deletion
        # operations will be performed for this model.

    class ReportTemplate(models.TextChoices):
        DEFAULT = "DEFAULT", _("Default template")

    RCC_file = models.FileField()
    render_pdf = models.BooleanField(blank=False, default=True)

    template = models.CharField(
        max_length=100,
        choices=ReportTemplate.choices,
        default=ReportTemplate.DEFAULT,
    )

    rna_metadata = JSONField(
        schema={
            "type": "object",
            "title": "RNA File",
            "keys": {
                "platform id": {
                    "type": "string",
                },
                "center id": {
                    "type": "string",
                },
                "concentration": {
                    "type": "number",
                },
                "units": {
                    "type": "string",
                    "default": "ng/ul",
                },
                "260/280 ratio": {
                    "type": "number",
                },
                "260/230 ratio": {
                    "type": "number",
                },
            },
        },
        default=None,
        blank=True,
        null=True,
    )

    patient_metadata = JSONField(
        schema={
            "type": "object",
            "title": "Free JSON key-values",
            "keys": {},
            "additionalProperties": {"type": "string"},
        },
        default=None,
        blank=True,
        null=True,
    )

    def get_report(self):

        style = "pdf" if self.render_pdf else "html"

        url = urljoin(settings.HISTOMX_SERVICE_URL, f"histomx_report/{style}")
        response = requests.post(
            url,
            json=dict(
                rccdata=self.RCC_file.read().decode("utf8"),
                template=self.template,
                rna_metadata=self.rna_metadata or {},
                patient_metadata=self.patient_metadata or {},
            ),
        )

        if response.status_code != 200:
            print(response.content)
            raise ValueError("Probably not a valid RCC file.")

        return response.content, response.headers["content-type"]
