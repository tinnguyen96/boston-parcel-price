library(tidyverse)

source("preprocess_lib.R")

dirname <- "~/Datasets/property-assessment/"

# we use the residential parts of land use codes from 
# https://www.cityofboston.gov/images_documents/land_use_codes[1]_tcm3-8867.pdf

LUs <- c("R1","R2","R3","R4","A","RL","CD")

vnames <- c("PID","LIVING_AREA", "LU", "ZIPCODE", "TOTAL_VALUE","YEAR")

dflist <- list()
for (yr in c(2014:2023)) {
  df <- processData(dirname, yr)
  dflist[[length(dflist) + 1]] <- df %>% dplyr::select(all_of(vnames))
}
finaldf <- bind_rows(dflist)

finaldf <- cleanData(finaldf, LUs)
# 
write.csv(finaldf, "combineddf.csv", row.names=FALSE)

finaldf %>% pull(LU) %>% unique() %>% print()

