import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from icdot.users.models import UserScopedModel


class Transplant(UserScopedModel):
    # WARNING: We use views/forms with fields='__all__'.
    # Please make sure when adding fields here that it is okay for users to both
    # see and edit them without it being a security problem for the app!

    class Sex(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        OTHER = "other", _("other")

    class WeightUnits(models.TextChoices):
        KG = "kg", _("kilograms (kg)")
        POUNDS = "lbs", _("pounds (lb)")

    class HeightUnits(models.TextChoices):
        CM = "cm", _("centimeters (cm)")
        METERS = "m", _("meters (m)")
        IN = "in", _("inches (in)")
        FEET = "ft", _("feet (ft)")

    class Ethnicity(models.TextChoices):
        AMERINDIAN = "American Indian or Alaska Native", _(
            "American Indian or Alaska Native)"
        )
        ASIAN = "Asian", _("Asian")
        BLACK = "Black or African American", _("Black or African American")
        LATINO = "Hispanic or Latino", _("Hispanic or Latino")
        PACIFIC = "Pacific Islander", _("Pacific Islander")
        WHITE = "white", _("white")
        OTHER = "other", _("other")

    class CreatinemiaUnits(models.TextChoices):
        UMOL_L = "umol/L", _("umol/L")
        MG_L = "mg/L", _("mg/L")

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

    class GraftFailureCause(models.TextChoices):
        DEATH = "death", _("death")
        INFECTION = "infection", _("infection")
        RECURRENT_DISEASE = "recurrent disease", _("recurrent disease")
        REJECTION = "rejection", _("rejection")

    class PreviousTransplant(models.TextChoices):
        NO = "no", _("no")
        HEART = "heart", _("heart")
        KIDNEY = "kidney", _("kidney")
        LIVER = "liver", _("liver")
        LUNG = "lung", _("lung")
        COMBINED = "combined transplant", _("combined transplant")

    class PrimaryDisease(models.TextChoices):
        AMYLOIDOSIS = "amyloidosis", _("amyloidosis")
        ANCA = "ANCA vasculitis", _(
            "anti-neutrophil cytoplasmic autoantibody (ANCA) vasculitis"
        )
        CAKUT = "CAKUT", _("congenital abnormality of the kidney or urinary tract (CAKUT)")
        CPN = "CPN", _("chronic progressive nephropathy (CPN)")
        C3_GLOMERULOPATHY = "complement 3 glomerulopathy", _(
            "complement 3 glomerulopathy"
        )
        DIABETES = "diabetes mellitus", _("diabetes mellitus")
        DIABETIC_NEPHROPATHY = "diabetic nephropathy", _("diabetic nephropathy")
        FSGS = "FSGS", _("focal segmental glomerulosclerosis (FSGS)")
        GLOMERULAR_NEPHROPATHY = "glomerular nephropathy", _("glomerular nephropathy")
        HKD = "hypertensive kidney disease", _("hypertensive kidney disease")
        IGA_NEPHROPATHY = "IgA nephropathy", _("IgA nephropathy")
        PYELO = "interstitial nephropathy/pyelonephritis", _(
            "interstitial nephropathy/pyelonephritis"
        )
        MPGN = "MPGN", _("Membranoproliferative glomerulonephritis (MPGN)")
        MIDD = "MIDD", _("Monoclonal immunoglobulin (Ig) deposition disease (MIDD)")
        VASCULAR_NEPHROPATHY = "vascular nephropathy", _("vascular nephropathy")
        ALPORT = "alport syndrome", _("alport syndrome")
        FABRY = "fabry disease", _("fabry disease")
        PKD = "polycystic kidney disease", _("polycystic kidney disease")
        CONGENITAL = "congenital nephropathy", _("congenital nephropathy")

    class DonorCriteria(models.TextChoices):
        SCD = "SCD", _("Standard Donor Criteria (SCD)")
        ECD = "ECD", _("Expanded Donor Criteria (ECD)")

    class DonorType(models.TextChoices):
        LIVING = "living donor", _("living donor")
        DECEASED = "deceased donor", _("deceased donor")

    class LivingDonorType(models.TextChoices):
        UNRELATED = "unrelated", _("unrelated donor")
        RELATED_HLA_IDENTICAL = "related HLA identical", _("related HLA identical donor")
        RELATED_HLA_NON_IDENTICAL = "related non-HLA identical", _("related non-HLA identical donor")

    class DeceasedDonorType(models.TextChoices):
        DBD = "DBD", _("donation after brain death (DBD)")
        DCD = "DCD", _("donation after circulatory death (DCD)")

    class CauseDeath(models.TextChoices):
        ANOXIA = "anoxia", _("anoxia")
        STROKE = "cerebrovascular/stroke", _("cerebrovascular/stroke")
        TUMOR = "CNS tumor", _("CNS tumor")
        TRAUMA = "head trauma", _("head trauma")

    class TimeUnits(models.TextChoices):
        MINUTES = "minutes", _("minutes")
        HOURS = "hours", _("hours")
        MONTHS = "months", _("months")
        DAYS = "days", _("days")
        YEARS = "years", _("years")

    class InductionTherapy(models.TextChoices):
        ATG = "ATG", _("thymoglbulin (ATG)")
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

    class PreTransplantBiopsyType(models.TextChoices):
        PRE_IMPLANT = "pre-implantation", _("pre-implantation")
        PROCUREMENT = "procurement", _("procurement")

    # Main information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transplant_date = models.DateField()
    donor_ref = models.CharField(max_length=256)
    recipient_ref = models.CharField(max_length=256)

    # Recipient information
    recipient_record_date = models.DateField(
        blank=True,
        null=True,
    )
    recipient_dob = models.DateField(
        blank=True,
        null=True,
    )
    recipient_age = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="recipient age (years)",
    )
    recipient_height = models.FloatField(
        blank=True,
        null=True,
        verbose_name="recipient height",
    )
    recipient_height_units = models.CharField(
        max_length=50,
        default=HeightUnits.CM,
        choices=HeightUnits.choices,
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
    time_on_dialysis_units = models.CharField(
        blank=True,
        max_length=50,
        choices=TimeUnits.choices,
    )
    previous_transplant = models.CharField(
        max_length=100,
        choices=PreviousTransplant.choices,
        blank=True,
    )
    primary_kidney_disease = models.CharField(
        max_length=200,
        blank=True,
        choices=PrimaryDisease.choices,
        verbose_name="primary kidney disease",
    )
    recipient_cmv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Cytomegalovirus status",
    )
    recipient_ebv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Epstein-Barr virus status",
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
    recipient_hiv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="HIV status",
    )
    # Outcomes
    recipient_death_date = models.DateField(
        blank=True,
        null=True,
    )
    graft_failure_date = models.DateField(
        blank=True,
        null=True,
    )
    graft_failure_cause = models.CharField(
        max_length=100,
        blank=True,
        choices=GraftFailureCause.choices,
    )
    # Donor information
    donor_record_date = models.DateField(
        blank=True,
        null=True,
    )
    donor_dob = models.DateField(
        blank=True,
        null=True,
    )
    donor_age = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="donor age (years)",
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
    donor_egfr = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(120.0)],
        blank=True,
        null=True,
        verbose_name="Donor eGFR (mL/min/1.73m2)",
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
    donor_creatinemia = models.FloatField(
        blank=True,
        null=True,
    )
    donor_creatinemia_units = models.CharField(
        max_length=50,
        default=CreatinemiaUnits.UMOL_L,
        choices=CreatinemiaUnits.choices,
    )
    donor_cmv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="cytomegalovirus status",
    )
    donor_ebv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Epstein-Barr virus status",
    )
    donor_hcv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="hepatitus C status",
    )
    donor_hiv_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="HIV status",
    )
    # Graft
    procurement_date = models.DateField(
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
        verbose_name="total HLA-A mismatches",
    )
    hla_b_mismatches = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="total HLA-B mismatches",
    )
    hla_dr_mismatches = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="total HLA-DR mismatches",
    )
    cold_ischemia_time = models.FloatField(
        blank=True, null=True, verbose_name="Cold Ischemia Time (CIT)"
    )
    cold_ischemia_time_units = models.CharField(
        blank=True,
        max_length=50,
        choices=TimeUnits.choices,
    )
    delayed_graft_function = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="delayed graft function (DGF)",
    )
    induction_therapy = models.CharField(
        max_length=100,
        blank=True,
        choices=InductionTherapy.choices,
        verbose_name="induction therapy",
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
        verbose_name=" iDSA class", # temporary hack to prevent auto-capitalization
    )
    i_dsa_specificity = models.CharField(
        blank=True,
        max_length=50,
        choices=iDSAspecifiity.choices,
        verbose_name=" iDSA specificity",
    )
    i_dsa_mfi = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=" iDSA MFI",
    )
    c1q_binding = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="C1q binding",
    )
    # Day 0 biopsy
    pre_transplant_biopsy_type = models.CharField(
        max_length=100,
        choices=PreTransplantBiopsyType.choices,
        blank=True,
    )
    ci_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name=" ci score",  # temporary hack to prevent auto-capitalization
    )
    ct_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name=" ct score",
    )
    cv_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name=" cv score",
    )
    ah_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name=" ah score",
    )
    percent_glomerulosclerosis = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        blank=True,
        null=True,
        verbose_name="percent sclerotic glomeruli",
    )

    def __str__(self):
        return f"{self.transplant_date} from {self.donor_ref} to {self.recipient_ref}"
