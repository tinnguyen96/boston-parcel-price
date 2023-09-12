
cleanData <- function(df, LUs) {
  # Input:
    # df: data frame with columns
      # PID, ZIPCODE, TOTAL_VALUE, YEAR, LIVING_AREA, GROSS_AREA
    # LUs: vector of strings (land use codes)
  
  # Input:
  
  df <- df %>% 
    dplyr::filter(LU %in% LUs)
  
  return(df)
}

processData <- function(dataDir, yr) {
  # Input:
    # dataDir: str
    # yr: scalar
  # Output:
    # df: data frame with columns
      # PID, ZIPCODE, TOTAL_VALUE, YEAR, GROSS_AREA, LIVING_AREA (among others)
  if (yr %in% c(2014, 2015, 2016, 2017))  {
    fname <- sprintf("property-assessment-fy%d.csv", yr)
    df <- read.csv(paste0(dataDir, fname))
    if (yr == 2014) {
      df <- df %>% mutate(PID = str_replace_all(Parcel_ID,"_",""))
    } else {
      df <- df %>% mutate(PID = str_replace_all(PID,"_",""))
    }
    df <- df %>% 
      mutate(ZIPCODE = str_replace_all(ZIPCODE,"_","")) %>% 
      mutate(TOTAL_VALUE = as.numeric(AV_TOTAL))
    
  } else if (yr == 2018) {
    fname <- "ast2018full.csv"
    df <- read.csv(paste0(dataDir, fname))
    df <- df %>%
      mutate(PID = as.character(PID)) %>%
      mutate(ZIPCODE = paste0("0",as.character(ZIPCODE))) %>%
      mutate(TOTAL_VALUE = as.numeric(AV_TOTAL))
    
  } else if (yr == 2019) {
    fname <- "fy19fullpropassess.csv"
    df <- read.csv(paste0(dataDir, fname))
    df <- df %>% 
      mutate(PID = as.character(PID)) %>% 
      mutate(ZIPCODE = paste0("0",as.character(ZIPCODE))) %>%
      mutate(TOTAL_VALUE = as.numeric(AV_TOTAL))
    
  } else if (yr == 2020) {
    fname <- "data2020-full.csv"
    df <- read.csv(paste0(dataDir, fname))
    df <- df %>% 
      mutate(PID = as.character(PID)) %>% 
      mutate(ZIPCODE = paste0("0",as.character(ZIPCODE))) %>%
      mutate(TOTAL_VALUE = as.numeric(AV_TOTAL))
    
  } else if (yr == 2021) {
    fname <- "data2021-full.csv"
    df <- read.csv(paste0(dataDir, fname))
    df <- df %>% 
      mutate(PID = as.character(PID)) %>% 
      mutate(ZIPCODE = paste0("0",as.character(ZIPCODE))) %>%
      mutate(TOTAL_VALUE = str_replace_all(TOTAL_VALUE,"\\$","")) %>% 
      mutate(TOTAL_VALUE = str_replace_all(TOTAL_VALUE,",","")) %>% 
      mutate(TOTAL_VALUE = str_replace_all(TOTAL_VALUE," ","")) %>% 
      mutate(TOTAL_VALUE = as.numeric(TOTAL_VALUE))
    
  } else if (yr == 2022) {
    fname <- "fy2022pa-4.csv"
    df <- read.csv(paste0(dataDir, fname))
    df <- df %>% 
      mutate(PID = as.character(PID)) %>% 
      mutate(ZIPCODE = paste0("0",as.character(ZIPCODE))) %>% 
      mutate(TOTAL_VALUE = as.numeric(str_replace_all(TOTAL_VALUE,",","")))
    
  } else if (yr == 2023) {
    fname <- "fy2023-property-assessment-data.csv"
    df <- read.csv(paste0(dataDir, fname))
    df <- df %>% 
      mutate(PID = as.character(PID)) %>% 
      mutate(ZIPCODE = paste0("0",as.character(ZIP_CODE))) %>%
      mutate(TOTAL_VALUE = as.numeric(str_replace_all(TOTAL_VALUE,",","")))
  }
  df <- df  %>% mutate(YEAR=as.integer(yr))
  return(df)
}