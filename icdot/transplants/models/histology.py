import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from icdot.transplants.models.biopsy import Biopsy
from icdot.users.models import UserScopedModel


class Histology(UserScopedModel):
    class Meta:
        verbose_name_plural = "histology"

    class ClinicalBiopsyIndication(models.TextChoices):
        PROTOCOL = "protocol", _("protocol")
        DGF = "DGF", _("Delayed Graft Function")
        SD = "slow deterioration", _(
            "slow deterioration (progressive increase in serum creatinine over time)"
        )
        ARF = "ARF", _("Acute Renal Failure")
        PROT_U = "proteinuria", _("proteinuria")
        HEMATURIA = "hematuria", _("hematuria")
        SUSP_AR = "SUSP_AR", _("Suspicious for acute rejection")
        SUSP_PVN = "SUSP_PVN", _("Suspicious for Polyoma Virus Nephropathy")
        TRANSPLANTECTOMY = "Transplantectomy", _("Transplantectomy biopsy")
        DENOVO_DSA = "de novo DSA", _("de novo DSA")
        FOLLOWUP = "follow-up", _("follow-up from previous biopsy")
        # other:specify

    class BiopsyAssessment(models.TextChoices):
        FROZEN = "frozen", _("frozen")
        PARAFFIN = "paraffin", _("paraffin")
        EM = "electron microscopy", _("electron microscopy")

    class BiopsyMethod(models.TextChoices):
        CORE = "core", _("core")
        NEEDLE = "needle", _("needle")
        WEDGE = "wedge", _("wedge")

    class TissueTechnique(models.TextChoices):
        FROZEN = "frozen", _("frozen")
        PARAFFIN = "paraffin", _("paraffin")
        AFA = "acidified formal alcohol", _("acidified formal alcohol (AFA)")

    class FSGStype(models.TextChoices):
        CELLULAR = "cellular", _("cellular")
        COLLAPSING = "collapsing", _("collapsing")
        NOS = "not otherwise specified", _("not otherwise specified (NOS)")
        PERIHILIAR = "perihiliar", _("perihiliar")
        TIP = "tip", _("tip")

    class BiopsyQuality(models.TextChoices):
        ADEQUATE = "adequate", _("adequate")
        MINIMAL = "minimal", _("minimal")

    class TMAlocation(models.TextChoices):
        ARTERIOLAR = "arteriolar", _("arteriolar")
        GLOMERULAR = "glomerular", _("glomerular")
        BOTH = "both", _("both")

    class InterstitialInflammation(models.TextChoices):
        NO = "no", _("no")
        MINIMAL = "minimal", _("minimal")
        MODERATE = "moderate", _("moderate")
        EXTENSIVE = "extensive", _("extensive")

    class EDDlocation(models.TextChoices):
        MESANGIAL = "mesangial", _("mesangial")
        SUBEPITHELIAL = "subepithelial", _("subepithelial")
        SUBENDOTHELIAL = "subendothelial", _("subendothelial")

    class EndothelialActivation(models.TextChoices):
        HYPERTROPHY = "hypertrophy", _("hypertrophy")
        LOSS_FENESTRATION = "loss of fenestrations", _("loss of fenestrations")
        SUBENDO_LUCENCY = "subendothelial lucency", _("subendothelial lucency")

    class TransplantGlomerulopathy(models.TextChoices):
        CG0 = "cg0", _("cg0")
        CG1A = "cg1a", _("cg1a")
        CG1B = "cg1b", _("cg1b")
        CG2 = "cg2", _("cg2")
        CG3 = "cg3", _("cg3")

    class PTCML(models.TextChoices):
        NORMAL = "normal", _("normal (<3 layers)")
        MODERATE = "3-6 layers ", _("3-6 layers ")
        SEVERE = "≥7 layers and ≥5 in at least 2", _(
            "≥7 layers in one cortical PTC and ≥5 layers in two additional capillaries "
        )

    class StainingIntensity(models.TextChoices):
        ZERO = "0", _("0")
        PLUS_1 = "+", _("+")
        PLUS_2 = "++", _("++")
        PLUS_3 = "+++", _("+++")

    class PatternLocation(models.TextChoices):
        GRANULA_CAP_WALL = "granular/capillary wall", _("granular/capillary wall")
        GRANULAR_MESANGIAL = "granular/mesangial", _("granular/mesangial")
        LINEAR_CAP_WALL = "linear/capillary wall", _("linear/capillary wall")
        LINEAR_MESANGIAL = "linear/mesangial", _("linear/mesangial")

    class FibrinDeposition(models.TextChoices):
        CRESCENT = "crescent", _("crescent")
        INTERSTITIAL = "interstitial", _("interstitial")
        MESANGIAL = "mesangial", _("mesangial")
        SEG_GLOMERULI = "segmental glomeruli", _("segmental glomeruli")

    class PrincipalDx(models.TextChoices):
        INADEQUATE = "inadequate for diagnosis", _("inadequate for diagnosis")
        NORMAL = "normal", _("normal")
        NER = "no evidence of rejection", _("no evidence of rejection")
        AAMR = "active AMR", _("active AMR")
        CAAMR = "chronic active AMR", _("chronic active AMR")
        CAMR = "chronic AMR", _("chronic AMR")
        ATCMR = "acute TCMR", _("acute TCMR")
        CATCMR = "chronic active TCMR", _("chronic active TCMR")
        MIXED = "mixed rejection", _("mixed rejection")
        C4DNER = "C4dNER", _("C4d with no evidence of rejection")
        PVN = "polyomavirus nephropathy", _("polyomavirus nephropathy")
        CNIT = "CNI toxicity", _("CNI toxicity")
        RECUR_GN = "recurrent glomerulonephritis", _("recurrent glomerulonephritis")
        DENOVO_GN = "de novo glomerulonephritis", _("de novo glomerulonephritis")
        ATI = "acute tubular injury", _("acute tubular injury (ATI)")
        DONOR_DISEASE = "donor disease", _("donor disease")
        IFTA_NOS = "IFTA NOS", _("IFTA NOS")
        ARTERIOSCLEROSIS = "Arteriosclerosis", _("arteriosclerosis")

    class RejectionDx(models.TextChoices):
        NER = "no evidence of rejection", _("no evidence of rejection")
        INADEQUATE = "inadequate for assessment of rejection", _(
            "inadequate for assessment of rejection"
        )
        # AMR
        AAMR = "active AMR", _("active AMR")
        CAAMR = "chronic active AMR", _("chronic active AMR")
        CAMR = "chronic AMR", _("chronic AMR")
        ATCMR = "acute TCMR", _("acute TCMR")
        CATCMR = "chronic active TCMR", _("chronic active TCMR")
        MIXED = "mixed rejection", _("mixed rejection")
        C4D_NER = "C4d NER", _(
            "C4D deposition without morphologic evidence for active rejection"
        )
        # TCMR
        BORDERLINE = "Borderline TCMR", _("Borderline/Suspicious for acute TCMR")
        ATCMR_IA = "acute TCMR IA", _("acute TCMR IA")
        ATCMR_IB = "acute TCMR IB", _("acute TCMR IB")
        ATCMR_IIA = "acute TCMR IIA", _("acute TCMR IIA")
        ATCMR_IIB = "acute TCMR IIB", _("acute TCMR IIB")
        ATCMR_III = "acute TCMR III", _("acute TCMR III")
        CATCMR_IA = "chronic active TCMR IA", _("chronic active TCMR IA")
        CATCMR_IB = "chronic active TCMR IB", _("chronic active TCMR IB")
        CATCMR_II = "chronic active TCMR II", _("chronic active TCMR II")

    class NonRejectionDx(models.TextChoices):
        NORMAL = "Normal biopsy or nonspecific changes", _(
            "Normal biopsy or nonspecific changes"
        )
        INADEQUATE = "inadequate for  assessment of rejection", _(
            "inadequate for  assessment of rejection"
        )
        REJECTION_ONLY = "Rejection only-no additional pathological abnormalities", _(
            "Rejection only-no additional pathological abnormalities"
        )
        OTHER = "other pathology", _("other pathology")
        GLOMERULAR_ISCHEMIA = "glomerular ischemia", _("glomerular ischemia")
        INFARCTION = "infarction", _("infarction")
        # acute tubular injury
        ATI = "ATI: not otherwise specified", _("ATI: not otherwise specified")
        ATI_SUSP_CNIT = "ATI: suspicious for CNI toxicity", _(
            "ATI: suspicious for CNI toxicity"
        )
        # (Thrombotic) microangiopathy (glomerular and/or arterial/arteriolar)
        TMA_NOS = "TMA: not otherwise specified", _("TMA: not otherwise specified")
        ACUTE_GI = "TMA: acute glomerular involvement", _(
            "TMA: acute glomerular involvement on LM"
        )
        SUBACUTE_ACUTE_GI = "TMA: subacute/chronic glomerular involvement on LM", _(
            "TMA: subacute/chronic glomerular involvement on LM"
        )
        ACUTE_AI = "TMA: acute arteriolar/arterial involvement", _(
            "TMA: acute arteriolar/arterial involvement on LM"
        )
        SUBACUTE_ACUTE_AI = (
            "TMA: subacute/chronic arteriolar/arterial involvement on LM",
            _("TMA: subacute/chronic arteriolar/arterial involvement on LM"),
        )
        EM_ONLY = "TMA: EM features only", _("TMA: EM features only")
        # IFTA
        IFTA_NOS = "IFTA: NOS", _("IFTA: not otherwise specified")
        IFTA1 = "IFTA1: Mild", _("IFTA1: Mild")
        IFTA2 = "IFTA2: Moderate", _("IFTA2: Moderate")
        IFTA3 = "IFTA3: Severe", _("IFTA3: Severe")
        # Significant (moderate to severe) vascular pathology
        SIG_VASCULAR_PATH = "Significant vascular pathology", _(
            "Significant vascular pathology"
        )
        SIG_AIT = "Significant arterial intimal thickening", _(
            "Significant arterial intimal thickening"
        )
        AIF = "arterial intimal fibrosis (non-inflammatory)", _(
            "Arterial intimal fibrosis (non-inflammatory)"
        )
        AIF_NO_FE = "arterial intimal thickening without fibroelastosis", _(
            "Arterial intimal thickening without fibroelastosis (at least partially)"
        )
        SIG_AH = "significant arteriolar hyalinosis", _(
            "significant arteriolar hyalinosis"
        )
        SIG_AH_DD = "significant arteriolar hyalinosis-likely donor-derived", _(
            "significant arteriolar hyalinosis-likely donor-derived"
        )
        SIG_AH_CNIT = (
            "significant arteriolar hyalinosis - suspicious for CNI toxicity",
            _("significant arteriolar hyalinosis - suspicious for CNI toxicity"),
        )
        # infection
        INFECTION = "infection: not otherwise specified", _(
            "infection: not otherwise specified"
        )
        PN = "infection: neutrophilic pyelonephritis/Suspicious for pyelonephritis", _(
            "infection: neutrophilic pyelonephritis/Suspicious for pyelonephritis"
        )
        BKV = "infection: BK virus nephropathy", _("infection: BK virus nephropathy")
        GRANULOMATOUS = "infection: granulomatous", _("infection: granulomatous")
        PVN_1 = "Polyomavirus Nephropathy Class 1", _(
            "Polyomavirus Nephropathy Class 1"
        )
        PVN_2 = "Polyomavirus Nephropathy Class 2", _(
            "Polyomavirus Nephropathy Class 2"
        )
        PVN_3 = "Polyomavirus Nephropathy Class 3", _(
            "Polyomavirus Nephropathy Class 3"
        )
        # glomerular disease
        GD_NOS = "glomerular disease: not otherwise specified"
        GD_IC_NOS = "glomerular disease: immune complex, not otherwise specified", _(
            "immune complex, not otherwise specifie"
        )
        GD_IC_IGA = "glomerular disease: immune complex, IgA", _("immune complex, IgA")
        GD_IC_MEMBRANOUS = "glomerular disease: immune complex, membranous", _(
            "glomerular disease: immune complex, membranous"
        )
        GD_IC_LUPUS = "glomerular disease: immune complex, Lupus nephritis", _(
            "glomerular disease: immune complex, Lupus nephritis"
        )
        GD_C3_G = "glomerular disease: C3 glomerulopathy", _("C3 glomerulopathy")
        GD_FSGS_NOS = "glomerular disease: FSGS", _("FSGS")
        GD_FSGS_RECUR = "glomerular disease: FSGS, likely recurrent", _(
            "FSGS, likely recurrent"
        )
        GD_DIABETIC_CHANGE = "glomerular disease: diabetic change", _(
            "glomerular disease: diabetic change"
        )
        GD_PPR = "glomerular disease: paraprotein-related", _(
            "glomerular disease: paraprotein-related"
        )
        # tubulointerstitial disease (non-rejection)
        TID = "tubulointerstitial disease: not otherwise specified", _(
            "tubulointerstitial disease"
        )
        TID_G_TIN = "tubulointerstitial disease: granulomatous TIN", _(
            "tubulointerstitial disease: granulomatous TIN"
        )
        TID_DI_TIN = "tubulointerstitial disease: drug-induced TIN", _(
            "tubulointerstitial disease: drug-induced TIN"
        )
        # neoplasia
        NEOPLASIA = "neoplasia: not otherwise specified", _("neoplasia")
        SUSP_NEOPLASIA = "preneoplasia/suspicious for neoplasia", _(
            "preneoplasia/suspicious for neoplasia"
        )
        NEOPLASIA_LPD = "post-transplant lymphoproliferative disease", _(
            "post-transplant lymphoproliferative disease"
        )

    # variables
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)

    # require: used to distinguish multiple biopsies
    histology_date = models.DateField()
    clinical_biopsy_indication = models.CharField(
        max_length=100,
        choices=ClinicalBiopsyIndication.choices,
        blank=True,
    )
    biopsy_assessment = models.CharField(
        max_length=100,
        choices=BiopsyAssessment.choices,
        blank=True,
    )
    biopsy_method = models.CharField(
        max_length=100,
        choices=BiopsyMethod.choices,
        blank=True,
    )
    tissue_technique = models.CharField(
        max_length=100,
        choices=TissueTechnique.choices,
        blank=True,
    )
    num_cores = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of cores",
    )
    num_glomeruli = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of glomeruli",
    )
    num_glomerulosclerosis = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of global glomerulosclerosis",
    )
    num_sclerotic_glomeruli = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of segmentally sclerotic glomeruli",
    )
    num_arteries = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of arteries",
    )
    biopsy_quality = models.CharField(
        max_length=100,
        blank=True,
        choices=BiopsyQuality.choices,
        verbose_name="Biopsy quality/adequacy",
    )
    fsgs_type = models.CharField(
        max_length=100,
        blank=True,
        choices=FSGStype.choices,
        verbose_name="FSGS type",
    )
    ati_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Acute Tubular Injury (ATI)",
    )
    tma_status = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Thrombotic Microangiopathy",
    )
    tma_location = models.CharField(
        max_length=100,
        choices=TMAlocation.choices,
        blank=True,
        verbose_name="TMA location",
    )
    # collapse: lesions
    # header: acute lesions
    g_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="glomerulitis (g)",
    )
    ptc_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="peritubular capillaritis (ptc)",
    )
    i_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="interstitial inflammation (i)",
    )
    t_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="tubulitis (t)",
    )
    v_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="intimal arteritis (v)",
    )
    # header: chronic lesions
    cg_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="Glomerular Basement Membrane double contours (cg)",
    )
    ci_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="interstitial fibrosis (ci)",
    )
    ct_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="tubular atrophy (ct)",
    )
    cv_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="vascular fibrous intimal thickening (cv))",
    )
    ah_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="artieriolar hyalinosis (ah)",
    )
    mm_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="mesangial matrix expansion (mm)",
    )
    # header: acute_chronic_lesions
    ti_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="total inflammation (ti)",
    )
    i_ifta_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="inflammation in the area of IFTA (i-IFTA)",
    )
    t_ifta_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="tubulitis in the area of IFTA (t-IFTA)",
    )
    percent_cortex_if = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
        verbose_name="percent cortex with inflammation and fibrosis",
    )
    percent_ifta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
        verbose_name="IFTA %",
    )
    chronic_allograft_arteriopathy = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="chronic allograft arteriopathy",
    )
    pvl_load_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        null=True,
        verbose_name="PVL (polyomavirus replication/load level)",
    )
    # collapse: immunohistochemsitry
    crescents = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        blank=True,
        null=True,
    )
    glomerular_thrombi = models.BooleanField(
        blank=True, null=True, verbose_name="glomerular thrombi"
    )
    arterial_thrombi = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="arterial/arteriolar thrombi",
    )
    plasma_cell_if = models.CharField(
        blank=True,
        max_length=50,
        choices=InterstitialInflammation.choices,
        verbose_name="interstitial inflammation by plasma cells",
    )
    eosinophil_cell_if = models.CharField(
        blank=True,
        max_length=50,
        choices=InterstitialInflammation.choices,
        verbose_name="interstitial inflammation by eosinophils",
    )
    sv40t = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="SV40-T",
    )
    other_ihc = models.CharField(
        blank=True,
        max_length=200,
        verbose_name="other immunohistochemistry (IHC)",
    )
    # collapse: electron_microscopy
    mesangial_hypercellularity = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="mesangial hypercellularity",
    )
    electron_dense_deposits = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="electron dense deposits",
    )
    edd_substructre = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="EDD substructure",
    )
    edd_location = models.CharField(
        max_length=100,
        blank=True,
        choices=EDDlocation.choices,
        verbose_name="EDD location",
    )
    gbm_duplication = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="GBM duplication",
    )
    endothelial_activation = models.CharField(
        max_length=100,
        blank=True,
        choices=EndothelialActivation.choices,
        verbose_name="endothelial activation",
    )
    transplant_glomerulopathy = models.CharField(
        max_length=100,
        blank=True,
        choices=TransplantGlomerulopathy.choices,
        verbose_name="transplant glomerulopathy (cg)",
    )
    ptcml = models.CharField(
        max_length=100,
        blank=True,
        choices=PTCML.choices,
        verbose_name="Peritubular Capillary Basement Membrane Multilayering (PTCML)",
    )
    other_em = models.CharField(
        blank=True,
        max_length=200,
        verbose_name="other electron microscopy (EM)",
    )
    # collapse: immunofluorescence
    igg_staining = models.CharField(
        max_length=10,
        blank=True,
        choices=StainingIntensity.choices,
        verbose_name="IgG staining",
    )
    igg_location = models.CharField(
        max_length=100,
        blank=True,
        choices=PatternLocation.choices,
        verbose_name="IgG pattern/location",
    )
    iga_staining = models.CharField(
        max_length=10,
        blank=True,
        choices=StainingIntensity.choices,
        verbose_name="IgA staining",
    )
    iga_location = models.CharField(
        max_length=100,
        blank=True,
        choices=PatternLocation.choices,
        verbose_name="IgA pattern/location",
    )
    igm_staining = models.CharField(
        max_length=10,
        blank=True,
        choices=StainingIntensity.choices,
        verbose_name="IgM staining",
    )
    igm_location = models.CharField(
        max_length=100,
        blank=True,
        choices=PatternLocation.choices,
        verbose_name="IgM pattern/location",
    )
    c1q_staining = models.CharField(
        max_length=10,
        blank=True,
        choices=StainingIntensity.choices,
        verbose_name="C1q staining",
    )
    c1q_location = models.CharField(
        max_length=100,
        blank=True,
        choices=PatternLocation.choices,
        verbose_name="C1q pattern/location",
    )
    c3_staining = models.CharField(
        max_length=10,
        blank=True,
        choices=StainingIntensity.choices,
        verbose_name="C3 staining",
    )
    c3_location = models.CharField(
        max_length=100,
        blank=True,
        choices=PatternLocation.choices,
        verbose_name="C3 pattern/location",
    )
    kappa_staining = models.CharField(
        max_length=10,
        blank=True,
        choices=StainingIntensity.choices,
        verbose_name="kappa staining",
    )
    kappa_location = models.CharField(
        max_length=100,
        blank=True,
        choices=PatternLocation.choices,
        verbose_name="kappa pattern/location",
    )
    lambda_staining = models.CharField(
        max_length=10,
        blank=True,
        choices=StainingIntensity.choices,
        verbose_name="lambda staining",
    )
    lambda_location = models.CharField(
        max_length=100,
        blank=True,
        choices=PatternLocation.choices,
        verbose_name="lambda pattern/location",
    )
    fibrin_deposition = models.CharField(
        max_length=100,
        blank=True,
        choices=FibrinDeposition.choices,
        verbose_name="fibrin deposition",
    )
    # collapse: histology_diagnosis
    principal_diagnosis = models.CharField(
        max_length=200,
        blank=True,
        choices=PrincipalDx.choices,
        verbose_name="principal diagnosis",
    )
    principal_diagnosis_other = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="principal diagnosis (other)",
    )
    rejection_diagnosis = models.CharField(
        max_length=200,
        blank=True,
        choices=RejectionDx.choices,
        verbose_name="rejection diagnosis",
    )  # choose at least 1; multiple choices allowed
    non_rejection_diagnosis = models.CharField(
        max_length=200,
        blank=True,
        choices=NonRejectionDx.choices,
        verbose_name="non-rejection diagnosis",
    )  # choose at least 1; multiple choices allowed
    diagnosis_comments = models.CharField(
        max_length=400,
        blank=True,
        verbose_name="diagnosis comments",
    )
