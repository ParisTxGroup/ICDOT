DEFAULT = (
    (
        None,
        {
            "fields": (
                "biopsy_date",
                ("biopsy_egfr", "biopsy_egfr_date"),
                ("biopsy_proteinuria", "biopsy_proteinuria_units"),
                (
                    "biopsy_proteinuria_dipstick",
                    "biopsy_proteinuria_dipstick_units",
                ),
                ("biopsy_creatinemia", "biopsy_creatinemia_units"),
                ("biopsy_creatinuria", "biopsy_creatinuria_units"),
                ("prot_creat_ratio", "prot_creat_ratio_units"),
                ("systolic_bp", "diastolic_bp"),
            ),
        },
    ),
    (
        "Treatment",
        {
            "classes": ("collapse",),
            "fields": (
                (
                    "immunosuppressants",
                    "immunosuppressant_dose",
                    "immunosuppressant_dose_units",
                ),
                ("immunosuppressant_trough", "immunosuppressant_postdose"),
                ("rejection_treatment", "treatment_start_date"),
                "treatment_response",
                "rejection_date",
            ),
        },
    ),
    (
        "Biomarkers",
        {
            "classes": ("collapse",),
            "fields": ("dd_cf_dna", "bkv_load", "cmv_load", "ebv_load"),
        },
    ),
    (
        "DSA",
        {
            "classes": ("collapse",),
            "fields": (
                "dsa_at_biopsy",
                "history_dsa",
                "immunodominant_dsa_class",
                "i_dsa_specificity",
                "i_dsa_mfi",
                "non_anti_hla_dsa",
                "non_anti_hla_dsa_type",
            ),
        },
    ),
)
