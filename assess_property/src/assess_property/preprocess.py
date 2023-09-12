import numpy as np
import pandas as pd
from tqdm import tqdm
import os

from assess_property.global_variables import LU_LIST, YR_TO_NAME, ZIPCODE_FILLNA, DATA_DIR

LB_YR_REMODEL = 1800
UB_YR_REMODEL = 2023
LB_YR_BUILT = 1800
UB_YR_BUILT = 2023

class RemoveOutlier:

    def __init__(self,
                df):
        self.df = df
        return

    def check_data(self):
        assert "YR_BUILT" in self.df
        assert "YR_REMODEL" in self.df
        assert "YEAR" in self.df
        return 

    def run(self):
        self.process_yearbuilt()
        self.process_yearremodel()
        return 

    def process_yearbuilt(self):
        mask = self.df["YR_BUILT"].notnull()
        self.df["YR_BUILT"] =  self.df["YR_BUILT"].mask(mask, lambda x: np.clip(x, a_min = LB_YR_BUILT, a_max = UB_YR_BUILT))
        return 
    
    def process_yearremodel(self):
        mask = self.df["YR_REMODEL"].notnull()
        self.df["YR_REMODEL"] =  self.df["YR_REMODEL"].mask(mask, lambda x: np.clip(x, a_min = LB_YR_REMODEL, a_max = UB_YR_REMODEL))
        return 
    

class ScaleTotalValue:

    def __init__(self,
                 df):
        self.df = df 
        return 
    
    def total_value_in_hundred_thousands(self):
        unit = 1e5
        self.df["TOTAL_VALUE_IN_HUNDRED_GRAND"] = self.df["TOTAL_VALUE"]/unit 
        return 
    
    def run(self):
        self.total_value_in_hundred_thousands()
        return 