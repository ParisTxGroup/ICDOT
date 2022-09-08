from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from icdot.utils.apppermissions import ensure_group_creation


class HistomxConfig(AppConfig):
    name = "icdot.histomx"
    verbose_name = _("Histomx")

    def ready(self):
        ensure_group_creation(self)
