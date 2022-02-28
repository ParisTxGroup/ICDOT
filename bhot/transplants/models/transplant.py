import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from bhot.users.models import UserScopedModel


class Transplant(UserScopedModel):

    # WARNING: We use views/forms with fields='__all__'.
    # Please make sure when adding fields here that it is okay for users to both
    # see and edit them without it being a security problem for the app!

    class Sex(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")

    class WeightUnits(models.TextChoices):
        KG = "kilograms", _("kilograms (kg)")
        POUNDS = "ounds", _("pounds (lb)")

    class HeightUnits(models.TextChoices):
        CM = "centimeters", _("centimeters (cm)")
        METERS = "meters", _("meters (m)")
        IN = "inches", _("inches (in)")
        FEET = "feet", _("feet (ft)")

    class Ethnicity(models.TextChoices):
        AMERINDIAN = "American Indian or Alaska Native", _(
            "American Indian or Alaska Native)"
        )
        ASIAN = "Asian", _("Asian")
        BLACK = "Black or African American", _("Black or African American")
        LATINO = "Hispanic or Latino", _("Hispanic or Latino")
        PACIFIC = "Pacific Islander", _("feet (ft)")
        WHITE = "white", _("white")

    class CreatinemiaUnits(models.TextChoices):
        UMOL_L = "umol/L", _("umol/L")
        MG_L = "mg/L", _("mgdL")

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

    class PreviousTransplant(models.TextChoices):
        NO = "no", _("no")
        HEART = "heart", _("heart")
        KIDNEY = "kidney", _("kidney")
        LIVER = "liver", _("liver")
        LUNG = "lung", _("lung")

    class PrimaryDisease(models.TextChoices):
        AMYLOIDOSIS = "amyloidosis", _("amyloidosis")
        ANCA = "anti-neutrophil cytoplasmic autoantibody (ANCA) vasculitis", _(
            "anti-neutrophil cytoplasmic autoantibody (ANCA) vasculitis"
        )
        CAKUT = "congenital abnormality of the kidney or urinary tract (CAKUT)", _(
            "congenital abnormality of the kidney or urinary tract (CAKUT)"
        )
        CPN = "chronic progressive nephropathy (CPN)", _(
            "chronic progressive nephropathy (CPN)"
        )
        C3_GLOMERULOPATHY = "complement 3 glomerulopathy", _(
            "complement 3 glomerulopathy"
        )
        DIABETES = "diabetes mellitus", _("diabetes mellitus")
        DIABETIC_NEPHROPATHY = "diabetic nephropathy", _("diabetic nephropathy")
        FSGS = "focal segmental glomerulosclerosis (FSGS)", _(
            "focal segmental glomerulosclerosis (FSGS)"
        )
        GLOMERULAR_NEPHROPATHY = "glomerular nephropathy", _("glomerular nephropathy")
        HKD = "hypertensive kidney disease", _("hypertensive kidney disease")
        IGA_NEPHROPATHY = "IgA nephropathy", _("IgA nephropathy")
        PYELO = "interstitial nephropathy/pyelonephritis", _(
            "interstitial nephropathy/pyelonephritis"
        )
        MPGN = "Membranoproliferative glomerulonephritis (MPGN)", _(
            "Membranoproliferative glomerulonephritis (MPGN)"
        )
        MIDD = "Monoclonal immunoglobulin (Ig) deposition disease (MIDD)", _(
            "Monoclonal immunoglobulin (Ig) deposition disease (MIDD)"
        )
        VASCULAR_NEPHROPATHY = "vascular nephropathy", _("vascular nephropathy")
        ALPORT = "alport syndrome", _("alport syndrome")
        FABRY = "fabry disease", _("fabry disease")
        PKD = "polycystic kidney disease", _("polycystic kidney disease")
        CONGENITAL = "congenital nephropathy", _("congenital nephropathy")

    class DonorCriteria(models.TextChoices):
        SCD = "SCD", _("Standard Donor Criteria")
        ECD = "ECD", _("Expanded Donor Criteria")

    class DonorType(models.TextChoices):
        LIVING = "living donor", _("living donor")
        DECEASED = "diseased donor", _("diseased donor")

    class LivingDonorType(models.TextChoices):
        UNRELATED = "unrelated donor", _("unrelated donor")
        RELATED_HLA_IDENTICAL = "related HLA identical donor", _(
            "related HLA identical donor"
        )
        RELATED_HLA_NON_IDENTICAL = "related non-HLA identical donor", _(
            "related non-HLA identical donor"
        )

    class DeceasedDonorType(models.TextChoices):
        DBD = "donation after brain death", _("donation after brain death")
        DCD = "donation after circulatory death", _("donation after circulatory death")

    class CauseDeath(models.TextChoices):
        ANOXIA = "anoxia", _("anoxia")
        STROKE = "cerebrovascular/stroke", _("cerebrovascular/stroke")
        TUMOR = "CNS tumor", _("CNS tumor")
        TRAUMA = "head trauma", _("head trauma")

    class TimeUnits(models.TextChoices):
        MINUTES = "minutes", _("minutes")
        HOURS = "hours", _("hours")
        DAYS = "days", _("days")

    class InductionTherapy(models.TextChoices):
        ATG = "thymoglbulin", _("thymoglbulin")
        BASILIXIMAB = "basiliximab", _("basiliximab")
        NONE = "none", _("none")

    class InductionTherapyUnits(models.TextChoices):
        MG_DAY = "mg/day", _("mg/day")
        MG_2X_DAY = "mg twice per day", _("mg twice per day")
        MG_WEEK = "mg per week", _("mg per week")
        MG_15_DAYS = "mg per 15 days", _("mg per 15 days")

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

    # Main information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transplant_date = models.DateField(
        blank=True,
        null=True,
    )
    donor_ref = models.CharField(max_length=256)
    recipient_ref = models.CharField(max_length=256)

    # Donor information
    donor_record_date = models.DateField()
    donor_dob = models.DateField(
        blank=True,
        null=True,
    )
    donor_age = models.IntegerField(
        blank=True,
        null=True,
    )
    donor_sex = models.CharField(
        max_length=1,
        choices=Sex.choices,
        blank=True,
    )
    donor_ethnicity = models.CharField(
        max_length=100,
        choices=Ethnicity.choices,
        blank=True,
    )
    procurement_date = models.DateField(
        blank=True,
        null=True,
    )
    donor_criteria = models.CharField(
        max_length=100,
        choices=DonorCriteria.choices,
        blank=True,
    )
    donor_type = models.CharField(
        max_length=100,
        choices=DonorType.choices,
        blank=True,
    )
    living_donor_type = models.CharField(
        max_length=100,
        choices=LivingDonorType.choices,
        blank=True,
    )
    deceased_donor_type = models.CharField(
        max_length=100,
        choices=DeceasedDonorType.choices,
        blank=True,
    )
    donor_death_cause = models.CharField(
        max_length=100,
        choices=CauseDeath.choices,
        blank=True,
    )
    donor_egfr = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(500.0)],
        blank=True,
        null=True,
        verbose_name="Donor eGFR (mL/min/1.73m2)",
    )
    donor_egfr_date = models.DateField(
        blank=True,
        null=True,
    )
    donor_proteinuria = models.FloatField(
        blank=True,
        null=True,
    )
    donor_proteinuria_units = models.CharField(
        max_length=50,
        choices=ProteinuriaUnits.choices,
        default=ProteinuriaUnits.G_G,
    )
    kdri = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        blank=True,
        null=True,
        verbose_name="Kidney Donor Risk Index",
    )
    donor_diabetes = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="donor diabetes status",
    )
    donor_hypertension = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="donor history of hypertension",
    )
    donor_comorbities = models.CharField(
        max_length=500,
        blank=True,
    )
    donor_creatinemia = models.FloatField(
        blank=True,
        null=True,
    )
    donor_creatinemia_units = models.CharField(
        max_length=50,
        default=CreatinemiaUnits.UMOL_L,
        choices=CreatinemiaUnits.choices,
    )
    donor_proteinuria = models.FloatField(
        blank=True,
        null=True,
    )
    donor_proteinuria_units = models.CharField(
        max_length=50,
        choices=ProteinuriaUnits.choices,
        default=ProteinuriaUnits.MG_DL,
    )
    donor_proteinuria_dipstick = models.CharField(
        max_length=20,
        blank=True,
        choices=ProtDipstick.choices,
    )
    donor_proteinuria_dipstick_units = models.CharField(
        max_length=50,
        default=ProtDipstickUnits.MG_DL_RANGE,
        choices=ProtDipstickUnits.choices,
    )
    donor_proteinuria_date = models.DateField(
        blank=True,
        null=True,
    )
    donor_aboi = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="ABO incompatible donor",
    )
    hla_a_mismatches = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="total HL-A mismatches",
    )
    hla_b_mismatches = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="total HL-A mismatches",
    )
    hla_dr_mismatches = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="total HL-A mismatches",
    )
    cold_ischemia_time = models.FloatField(
        blank=True,
        null=True,
        choices=TimeUnits.choices,
    )
    delayed_graft_function = models.BooleanField(
        blank=True, null=True, verbose_name="delayed graft function"
    )
    dgf_time = models.BooleanField(
        blank=True,
        null=True,
        choices=TimeUnits.choices,
        verbose_name="delayed graft function time",
    )
    induction_therapy = models.CharField(
        blank=True, choices=InductionTherapy.choices, verbose_name="induction therapy"
    )
    preformed_dsa = models.BooleanField(
        blank=True,
        null=True,
    )
    dsa_date = models.DateField(
        blank=True,
        null=True,
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

    # Recipient information
    recipient_record_date = models.DateField(
        blank=True,
        null=True,
    )
    recipient_dob = models.DateField(
        blank=True,
        null=True,
    )
    recipient_weight = models.FloatField(
        blank=True,
        null=True,
        verbose_name="recipient weight",
    )
    recipient_weight_units = models.CharField(
        max_length=50,
        default=WeightUnits.KG,
        choices=WeightUnits.choices,
    )
    recipient_height = models.FloatField(
        blank=True,
        null=True,
        verbose_name="recipient height",
    )
    recipient_weight_units = models.CharField(
        max_length=50,
        default=HeightUnits.CM,
        choices=HeightUnits.choices,
    )
    recipient_sex = models.CharField(
        max_length=1,
        choices=Sex.choices,
        blank=True,
    )
    recipient_ethnicity = models.CharField(
        max_length=100,
        choices=Ethnicity.choices,
        blank=True,
    )
    pre_transplant_dialysis = models.BooleanField(
        blank=True,
        null=True,
    )
    time_on_dialysis = models.IntegerField(
        blank=True,
        null=True,
    )
    previous_transplant = models.CharField(
        max_length=100,
        choices=PreviousTransplant.choices,
        blank=True,
    )
    recipient_hiv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="HIV status",
    )
    recipient_hbv_ag_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="HBV HBsAg status",
    )
    recipient_hbv_as_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="HBV HBsAs status",
    )
    recipient_hbv_ac_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="HBV HBsAc status",
    )
    recipient_hcv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Hepatitus C status",
    )
    recipient_systolic_bp = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="recipient systolic blood pressure (mm Hg)",
    )
    recipient_diastolic_bp = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="recipient diastolic blood pressure (mm Hg)",
    )
    primary_kidney_disease = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        choices=PrimaryDisease.choices,
        verbose_name="primary kidney disease",
    )
    recipient_egfr = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(500.0)],
        blank=True,
        null=True,
        verbose_name="recipient eGFR (mL/min/1.73m2)",
    )
    recipient_egfr_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="recipient eGFR date",
    )
    recipient_proteinuria = models.FloatField(
        blank=True,
        null=True,
    )
    recipient_proteinuria_units = models.CharField(
        max_length=50,
        choices=ProteinuriaUnits.choices,
        default=ProteinuriaUnits.MG_DL,
    )
    recipient_proteinuria_dipstick = models.CharField(
        max_length=20,
        blank=True,
        choices=ProtDipstick.choices,
    )
    recipient_proteinuria_dipstick_units = models.CharField(
        max_length=50,
        default=ProtDipstickUnits.MG_DL_RANGE,
        choices=ProtDipstickUnits.choices,
    )
    recipient_proteinuria_date = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.transplant_date} from {self.donor_ref} to {self.recipient_ref}"
