from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from icdot.utils.apppermissions import ensure_group_creation


class TransplantsConfig(AppConfig):
    name = "icdot.transplants"
    verbose_name = _("Transplants")

    def ready(self):
        ensure_group_creation(self)
