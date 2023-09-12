import numpy as np
import pandas as pd
from tqdm import tqdm
import os

from assess_property.global_variables import LU_LIST, YR_TO_NAME, ZIPCODE_FILLNA, DATA_DIR

class FormatDataFrame:
    def __init__(self, df, yr):
        """
        Input:
            df: data frame
            yr: int
        """
        self.df = df
        self.yr = yr
        return 

    def run(self):
        self.format_zipcode()
        self.format_pid()
        self.format_totalvalue()
        return 

    def format_pid(self):
        if self.yr in [2014, 2015, 2016, 2017]:
            if (self.yr == 2014):
                self.df["PID"] = self.df["Parcel_ID"].apply(lambda x: x.replace("_",""))
                self.df.drop(columns = ["Parcel_ID"], inplace=True)
            else:
                self.df["PID"] = self.df["PID"].apply(lambda x: x.replace("_",""))
        else:
            self.df["PID"] =  self.df["PID"].astype(str)
        return 

    def format_zipcode(self):
        if self.yr in [2014, 2015, 2016, 2017]:
            self.df["ZIPCODE"] = self.df["ZIPCODE"].astype(str)
            self.df["ZIPCODE"] = self.df["ZIPCODE"].apply(lambda x: x.replace("_",""))
    
        elif self.yr in [2018, 2019, 2020, 2021, 2022]:
            self.df["ZIPCODE"] = self.df["ZIPCODE"].apply(lambda x: "0%s" %x)
        
        elif self.yr == 2023:
            self.df["ZIP_CODE"] = self.df["ZIP_CODE"].fillna(ZIPCODE_FILLNA)
            self.df["ZIP_CODE"] = pd.to_numeric(self.df["ZIP_CODE"], downcast = "integer").astype(str)
            self.df["ZIPCODE"] = self.df["ZIP_CODE"].apply(lambda x: "0%s" %x)
        
        return 

    def format_totalvalue(self):
        if self.yr in [2014, 2015, 2016, 2017, 2018, 2019, 2020]:
            self.df["TOTAL_VALUE"] = pd.to_numeric(self.df["AV_TOTAL"], errors  = "coerce")
            self.df.drop(columns = ["AV_TOTAL"], inplace=True)
    
        elif (self.yr == 2021):
            self.df["TOTAL_VALUE"] = self.df["TOTAL_VALUE"].astype(str)
            self.df["TOTAL_VALUE"] = self.df["TOTAL_VALUE"].apply(lambda x: x.replace("$",""))
            self.df["TOTAL_VALUE"] = self.df["TOTAL_VALUE"].apply(lambda x: x.replace(",",""))
            self.df["TOTAL_VALUE"] = self.df["TOTAL_VALUE"].apply(lambda x: x.replace(" ",""))
            self.df["TOTAL_VALUE"] = pd.to_numeric(self.df["TOTAL_VALUE"], errors  = "coerce")
    
        elif (self.yr in  [2022, 2023]):
            self.df["TOTAL_VALUE"] = self.df["TOTAL_VALUE"].astype(str)
            self.df["TOTAL_VALUE"] = self.df["TOTAL_VALUE"].apply(lambda x: x.replace(",",""))
            self.df["TOTAL_VALUE"] = pd.to_numeric(self.df["TOTAL_VALUE"], errors  = "coerce")
        return 

class SaveYearDtype:

    def __init__(self,
                dirname,
                yrs):
        """
        Input:
            dirname: str
            yrs: list of int 
        """
        os.makedirs(dirname, exist_ok = True)
        self.dirname = dirname
        self.yrs = yrs
        return 

    def run(self):
        self.read_all_years()
        self.to_disk()
        return 

    def read_all_years(self):
        d_ = {}
        for yr in tqdm(self.yrs):
            fname = YR_TO_NAME[yr]
            path = "%s/%s" %(DATA_DIR, fname)
            df = pd.read_csv(path, low_memory = False)
            d_[yr] = df
        self.d_ = d_
        return 

    def to_disk(self):
        for key, val in self.d_.items():
            subdir = self.dirname + "/year=%d" %key
            os.makedirs(subdir, exist_ok = True)
            path = subdir + "/dtypes.csv"
            dtypedf =  val.dtypes.to_frame("dtype").reset_index().rename(columns = {"index":"var_name"})
            dtypedf.to_csv(path, index=False)
        return 

class ReadAllYears:

    def __init__(self,
                 yrs,
                 vnames):
        
        """
        """
        self.yrs = yrs
        self.vnames = vnames
        return 
    
    def read_all_years(self):
        dflist = []
        for yr in tqdm(self.yrs):
            fname = YR_TO_NAME[yr]
            path = "%s/%s" %(DATA_DIR, fname)
            df = pd.read_csv(path, low_memory = False)
            formatter = FormatDataFrame(df.copy(), yr)
            formatter.run()
            df = formatter.df.copy()
            df["YEAR"] = yr
            cols = []
            for vname in self.vnames:
                if vname in df.columns:
                    cols.append(vname)
            df = df[cols]
            dflist.append(df)
        df = pd.concat(dflist).reset_index(drop=True)
        self.df = df
        return 

    def check_data(self):
        return 

if __name__ == "__main__":
    yrs = range(2014, 2024)
    vnames = ["PID", "LIVING_AREA", "LU", "ZIPCODE", "TOTAL_VALUE","YEAR"]
    reader = ReadAllYears(yrs, vnames)
    reader.read_all_years()
    print(reader.df.head())
    print(reader.df.info())
