import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from icdot.transplants.models.biopsy import Biopsy
from icdot.transplants.models.file_upload import TrackFileUploadModel
from icdot.users.models import UserScopedModel


class SequencingData(UserScopedModel, TrackFileUploadModel):
    class Meta:
        verbose_name_plural = "sequencing data"

    class RunProtocol(models.TextChoices):
        SENSITIVE = "high sensitivity", _("high sensitivity")
        STANDARD = "standard", _("standard")

    class RNAstorage(models.TextChoices):
        FFPE = "FFPE", _("FFPE")
        RNALATER = "RNAlater", _("RNAlater")
        FROZEN = "frozen", _("frozen")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)

    sequencing_date = models.DateField()
    run_protocol = models.CharField(
        blank=True,
        max_length=50,
        choices=RunProtocol.choices,
    )
    rna_storage = models.CharField(
        max_length=100,
        choices=RNAstorage.choices,
        default=RNAstorage.FFPE,
        verbose_name="RNA storage",
    )
    rna_concentration = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        blank=True,
        null=True,
        verbose_name="RNA concentration (ng/ul)",
    )
    rna_integrity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True,
        verbose_name="RNA Integrity Number",
    )
    # RCC file

    # FIXME: Make this required.
    file_ref = models.CharField(
        max_length=256,
        blank=True,
        help_text=( # FIXME:
            "<b>This is the name that will be stored in the database for your RCC file.</b><br/>"
            "This reference will be matched against files that are uploaded as batches.<br/>"
            "You can also upload a file directly and it will be associated to this reference."
        ),
        verbose_name="file name"  # FIXME: This should be the actual name, including in excel.
    )
    file_path = models.FileField(
        null=True,
        editable=False,
    )

    TRACK_FILE_UPLOAD = {"file_ref": "file_path"}
