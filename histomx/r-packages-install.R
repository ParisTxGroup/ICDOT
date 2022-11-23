
required_packages <- c(
    "FactoMineR",
    "MLeval",
    "NormqPCR",
    "RCRnorm",
    "RUVSeq",
    "archetypes",
    "cowplot",
    "ggrepel",
    "kableExtra",
    "neighbr",
    "ordinal",
    "pROC",
    "prettydoc",
    "predtools",
    "reshape2",
    "rmarkdown",

    # New packages that haven't been added to pre-builts yet.
    "smotefamily",
    "ggpubr",
    "C50",
    "gbm",
    "xgboost",
    "DescTools"

)

installed_packages <- as.data.frame(installed.packages())$Package
to_install <- setdiff(required_packages, installed_packages)

# We want update=FALSE because we want to benefit from the installed
# pre-built packages and not re-install those.
BiocManager::install(to_install, update=FALSE, dependencies=TRUE, ask=FALSE, Ncpus=4)
