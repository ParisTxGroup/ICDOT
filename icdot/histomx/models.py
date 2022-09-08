from urllib.parse import urljoin

import requests
from django.conf import settings
from django.db import models


class HistomxReportRequest(models.Model):

    PROBABLY_NOT_AVAILABLE = settings.HISTOMX_SERVICE_URL is None

    class Meta:
        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

    RCC_file = models.FileField()
    render_pdf = models.BooleanField(blank=False, default=True)

    def get_report(self):

        style = "pdf" if self.render_pdf else "html"
        url = urljoin(settings.HISTOMX_SERVICE_URL, f"histomx_report/{style}")

        response = requests.post(
            url,
            files=dict(rccdata=self.RCC_file),
        )

        if response.status_code != 200:
            raise ValueError("Probably not a valid RCC file.")

        return response.content, response.headers["content-type"]
