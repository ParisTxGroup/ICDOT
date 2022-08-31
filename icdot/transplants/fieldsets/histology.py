DEFAULT = (
    (
        None,
        {
            "fields": (
                "biopsy",
                "histology_date",
                "biopsy_assessment",
                "biopsy_method",
                "tissue_technique",
                "num_cores",
                "num_glomeruli",
                "num_glomerulosclerosis",
                "num_sclerotic_glomeruli",
                "num_arteries",
                "biopsy_quality",
                "fsgs_type",
                "ati_status",
                ("tma_status", "tma_location"),
            ),
        },
    ),
    (
        "Banff lesions: acute",
        {
            "classes": ("collapse",),
            "fields": ("g_score", "ptc_score", "i_score", "t_score", "v_score"),
        },
    ),
    (
        "Banff lesions: chronic",
        {
            "classes": ("collapse",),
            "fields": (
                "cg_score",
                "ci_score",
                "ct_score",
                "cv_score",
                "ah_score",
                "mm_score",
            ),
        },
    ),
    (
        "Banff lesions: acute/chronic",
        {
            "classes": ("collapse",),
            "fields": (
                "ti_score",
                "i_ifta_score",
                "t_ifta_score",
                "percent_cortex_if",
                "percent_ifta",
                "chronic_allograft_arteriopathy",
                "pvl_load_level",
            ),
        },
    ),
    (
        "Immunohistochemistry",
        {
            "classes": ("collapse",),
            "fields": (
                "crescents",
                "glomerular_thrombi",
                "arterial_thrombi",
                "plasma_cell_if",
                "eosinophil_cell_if",
                "sv40t",
                "other_ihc",
            ),
        },
    ),
    (
        "Electron microscopy",
        {
            "classes": ("collapse",),
            "fields": (
                "mesangial_hypercellularity",
                "electron_dense_deposits",
                "edd_substructre",
                "edd_location",
                "gbm_duplication",
                "endothelial_activation",
                "transplant_glomerulopathy",
                "ptcml",
                "other_em",
            ),
        },
    ),
    (
        "Immunofluorescence",
        {
            "classes": ("collapse",),
            "fields": (
                ("igg_staining", "igg_location"),
                ("iga_staining", "iga_location"),
                ("igm_staining", "igm_location"),
                ("c1q_staining", "c1q_location"),
                ("c3_staining", "c3_location"),
                ("kappa_staining", "kappa_location"),
                ("lambda_staining", "lambda_location"),
                "fibrin_deposition",
            ),
        },
    ),
    (
        "Histology diagnosis",
        {
            "classes": ("collapse",),
            "fields": (
                "principal_diagnosis",
                "principal_diagnosis_other",
                "rejection_diagnosis",
                "non_rejection_diagnosis",
                "diagnosis_comments",
            ),
        },
    ),
)
