#!/usr/bin/env Rscript
if(!require(devtools)) install.packages("devtools")
if(!require(cutoff.scATOMIC)) devtools::install_github("inofechm/cutoff.scATOMIC", force = T)
if(!require(scATOMIC)) devtools::install_github("abelson-lab/scATOMIC", force = T)
install.packages("reticulate")

devtools::install_version("dlm", version = "1.1.5", repos = "http://cran.us.r-project.org")
devtools::install_version("Rmagic", version = "2.0.3", repos = "http://cran.us.r-project.org")
options(timeout=9999999)
devtools::install_github("abelson-lab/scATOMIC")

if(!require(Rmagic)) devtools::install_version("Rmagic", version = "2.0.3", repos = "http://cran.us.r-project.org")
