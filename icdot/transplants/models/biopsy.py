import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from icdot.transplants.models.transplant import Transplant
from icdot.users.models import UserScopedModel


class Biopsy(UserScopedModel):
    class Meta:
        verbose_name_plural = "biopsies"

    class CreatinemiaUnits(models.TextChoices):
        UMOL_L = "umol/L", _("umol/L")
        MG_L = "mg/L", _("mg/L")

    class CreatinuriaUnits(models.TextChoices):
        MMOL_L = "mmol/L", _("mmol/L")

    class ProteinuriaUnits(models.TextChoices):
        G_G = "g/g", _("g/g")
        G_24H = "g/24h", _("g/24h")
        MG_DL = "mg/dL", _("mg/dL")
        G_L = "g/L", _("g/L")
        MG_MMOL = "mg/mmol", _("mg/mmol")
        G_MMOL = "g/mmol", _("g/mmol")

    class ProtDipstick(models.TextChoices):
        ZERO = "0", _("0")
        PLUS_1 = "+", _("+")
        PLUS_2 = "++", _("++")
        PLUS_3 = "+++", _("+++")
        PLUS_4 = "++++", _("++++")

    class ProtDipstickUnits(models.TextChoices):
        MG_DL_RANGE = "mg/dL range", _("mg/dL range")

    class ProteinCreatinineRatioUnits(models.TextChoices):
        G_G = "g/g", _("g/g")

    class Immunosuppressants(models.TextChoices):
        ABATACEPT = "abatacept", _("abatacept")
        AZATHIOPRINE = "azathioprine", _("azathioprine")
        BELATACEPT = "belatacept", _("belatacept")
        CYCLOSPORINE = "cyclosporine", _("cyclosporine")
        EVEROLIMUS = "everolimus", _("everolimus")
        IDES = "IDeS", _("imlifidase (IDeS)")
        MMF = "MMF", _("mycophenolate mofetil (MMF)")
        MPA = "MPA", _("mycophenolic acid (MPA)")
        PREDNISONE = "prednisone", _("prednisone")
        SIROLIMUS = "sirolimus", _("sirolimus")
        TACROLIMUS = "tacrolimus", _("tacrolimus")
        OTHER = "other", _("other")

    class ImmunosuppressantDoseUnits(models.TextChoices):
        MG_DAY = "mg/day", _("mg/day")
        MG_2X_DAY = "mg twice per day", _("mg twice per day")
        MG_WEEK = "mg per week", _("mg per week")
        MG_15_DAYS = "mg per 15 days", _("mg per 15 days")
        # other:free text

    class BxRejectionTreatment(models.TextChoices):
        ALEMTUZUMAB = "alemtuzumab", _("alemtuzumab")
        BORTEZOMIB = "bortezomib", _("bortezomib")
        ATG = "ATG", _("anti-thymocyte globulin (ATG)")
        ECULIZUMAB = "eculizumab", _("eculizumab")
        IVIG = "IVIG", _("intravenous immunoglobulin (IVIG)")
        PLASMAPHARESIS = "plasmapharesis", _("plasmapharesis")
        RITUXIMAB = "rituximab", _("rituximab")

    class BxRejectionTreatmentResponse(models.TextChoices):
        COMPLETE = "complete", _("Complete response (Cr within 10% of baseline)")
        PARTIAL = "partial", _("Partial response (Cr 10-50% over baseline) ")
        NONE = "none", _("no response (Cr >50% increase over baseline)")

    class iDSAclass(models.TextChoices):
        CLASS_I = "I", _("I")
        CLASS_II = "II", _("II")
        CLASS_I_II = "I/II", _("I/II")

    class iDSAspecifiity(models.TextChoices):
        A = "A", _("A")
        B = "B", _("B")
        CW = "Cw", _("Cw")
        DR = "DR", _("DR")
        DQ = "DQ", _("DQ")
        DP = "DP", _("DP")

    class nonAntiHlaDsa(models.TextChoices):
        AT1R = "AT1R", _("AT1R")
        MICA = "MICA", _("MICA")
        ECXM = "ECXM", _("ECXM")
        VIMENTIN = "vimentin", _("vimentin")
        COLLAGEN = "collagen", _("collagen")
        KA1 = "K-a-1", _("K-a-1")
        TUBULIN = "tubulin", _("tubulin")
        OTHER = "other", _("other")

    class GraftFailureCause(models.TextChoices):
        DEATH = "death", _("death")
        INFECTION = "infection", _("infection")
        RECURRENT_DISEASE = "recurrent disease", _("recurrent disease")
        REJECTION = "rejection", _("rejection")

    # Main info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transplant = models.ForeignKey(Transplant, null=True, on_delete=models.SET_NULL)

    # transplant date?
    biopsy_date = models.DateField()
    biopsy_egfr = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(120.0)],
        blank=True,
        null=True,
        verbose_name="recipient eGFR (mL/min/1.73m2)",
    )
    biopsy_egfr_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="recipient eGFR date",
    )
    biopsy_proteinuria = models.FloatField(
        blank=True,
        null=True,
    )
    biopsy_proteinuria_units = models.CharField(
        max_length=50,
        choices=ProteinuriaUnits.choices,
        default=ProteinuriaUnits.MG_DL,
    )
    biopsy_proteinuria_dipstick = models.CharField(
        max_length=20,
        blank=True,
        choices=ProtDipstick.choices,
    )
    biopsy_proteinuria_dipstick_units = models.CharField(
        max_length=50,
        default=ProtDipstickUnits.MG_DL_RANGE,
        choices=ProtDipstickUnits.choices,
    )
    biopsy_creatinemia = models.FloatField(
        blank=True,
        null=True,
    )
    biopsy_creatinemia_units = models.CharField(
        max_length=50,
        default=CreatinemiaUnits.UMOL_L,
        choices=CreatinemiaUnits.choices,
    )
    biopsy_creatinuria = models.FloatField(
        blank=True,
        null=True,
    )
    biopsy_creatinuria_units = models.CharField(
        max_length=50,
        default=CreatinuriaUnits.MMOL_L,
        choices=CreatinuriaUnits.choices,
    )
    prot_creat_ratio = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(30.0)],
        blank=True,
        null=True,
        verbose_name="protein/creatinine ratio",
    )
    prot_creat_ratio_units = models.CharField(
        max_length=50,
        default=ProteinCreatinineRatioUnits.G_G,
        choices=ProteinCreatinineRatioUnits.choices,
    )
    systolic_bp = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="systolic blood pressure (mm Hg)",
    )
    diastolic_bp = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="diastolic blood pressure (mm Hg)",
    )
    # collapse: treatment
    immunosuppressants = models.CharField(
        max_length=100,
        blank=True,
        choices=Immunosuppressants.choices,
        verbose_name="immunosuppresants",
    )
    immunosuppressant_dose = models.FloatField(
        blank=True,
        null=True,
    )
    immunosuppressant_dose_units = models.CharField(
        max_length=100,
        blank=True,
        choices=ImmunosuppressantDoseUnits.choices,
        verbose_name="immunosuppresant dose units",
    )  # link immunosuppressant to dose (+ sign to add med + dose)
    immunosuppressant_trough = models.FloatField(
        blank=True,
        null=True,
        verbose_name="immunosuppressant trough level:C0 (ng/mL)",
    )
    immunosuppressant_postdose = models.FloatField(
        blank=True,
        null=True,
        verbose_name="immunosuppressant postdose level: C2 (ng/mL)",
    )
    rejection_treatment = models.CharField(
        max_length=100,
        choices=BxRejectionTreatment.choices,
        blank=True,
        verbose_name="rejection treatment",
    )
    treatment_start_date = models.DateField(
        blank=True,
        null=True,
    )  # link to treatment
    treatment_response = models.CharField(
        max_length=100,
        choices=BxRejectionTreatmentResponse.choices,
        blank=True,
        verbose_name="rejection treatment response",
    )
    rejection_date = models.DateField(
        blank=True,
        null=True,
    )
    # collapse: biomarkers
    dd_cf_dna = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        blank=True,
        null=True,
        verbose_name="donor-derived cf-DNA (%)",
    )
    bkv_load = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="BKV load (copies/mL)",
    )
    cmv_load = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="CMV load (copies/mL)",
    )
    ebv_load = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="EBV load (copies/mL)",
    )
    # collapse: dsa
    dsa_at_biopsy = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="DSA at time of biopsy",
    )
    history_dsa = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="history of DSA",
    )
    immunodominant_dsa_class = models.CharField(
        blank=True,
        max_length=50,
        choices=iDSAclass.choices,
        verbose_name="iDSA class",
    )
    i_dsa_specificity = models.CharField(
        blank=True,
        max_length=50,
        choices=iDSAspecifiity.choices,
        verbose_name="iDSA specificity",
    )
    i_dsa_mfi = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="iDSA MFI",
    )
    c1q_binding = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="C1q binding",
    )
    non_anti_hla_dsa = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="non anti-HLA DSA",
    )
    non_anti_hla_dsa_type = models.CharField(
        max_length=100,
        blank=True,
        choices=nonAntiHlaDsa.choices,
    )
