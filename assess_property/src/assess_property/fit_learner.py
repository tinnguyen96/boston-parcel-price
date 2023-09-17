
# Todos
# implement a percentage error score metric (if the price is 100k but we predict 90k, our error is 10%).

import numpy as np
import pandas as pd
from tqdm import tqdm
import os

from lightgbm import LGBMRegressor

import unittest

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_validate, KFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression

from assess_property.read_data import ReadAllYears
from assess_property.preprocess import RemoveOutlier, ScaleTotalValue
from assess_property.global_variables import LU_LIST, YR_TO_NAME, ZIPCODE_FILLNA, DATA_DIR


def MakeExperiment():
    """ 
    Experimental configs: 
    - use all data from 2014 through 2023 
    - use YR_BUILT, YEAR, YR_REMODEL, LIVING_AREA as features, and predict TOTAL_VALUE
    - 10-fold CV that treats all rows as iid 
    """

    # read data from disk 
    yrs = range(2014,2024)
    vnames = ["PID", "YR_REMODEL", "YR_BUILT", "LIVING_AREA", "LU", "ZIPCODE", "TOTAL_VALUE","YEAR"]
    reader = ReadAllYears(yrs, vnames)
    reader.read_all_years()

    # remove outiers 
    remover = RemoveOutlier(reader.df)
    remover.run()

    # scale total value column
    scaler = ScaleTotalValue(remover.df)
    scaler.run()

    # select only R1 code 
    df = scaler.df[scaler.df["LU"] == "R1"].copy()

    # CV experiment 
    var_names = ["YR_BUILT", 
                 "YEAR",
                 "YR_REMODEL",
                 "LIVING_AREA"]
    response_name = "TOTAL_VALUE_IN_HUNDRED_GRAND"
    random_seed = 0
    n_fold = 10
    cv_experiment = CV_Experiment(df, 
                        var_names, 
                        response_name, 
                        n_fold=n_fold,
                        random_seed = random_seed)
    cv_experiment.set_up()

    onefit_experiment = OneFit_Experiment(df, 
                        var_names, 
                        response_name, 
                        n_fold=n_fold,
                        random_seed = random_seed)
    onefit_experiment.set_up()

    return df, onefit_experiment, cv_experiment 


class Experiment:
    def __init__(self, 
                 df, 
                 var_names, 
                 response_name,
                 n_fold,
                 random_seed):
        self.df = df
        self.var_names = var_names
        self.response_name = response_name
        self.n_fold = n_fold
        self.random_seed = random_seed  
        return 
    
    def set_up(self):
        self.seperate_response_from_features()
        return 

    def seperate_response_from_features(self):
        X = self.df[self.var_names].to_numpy() # (N,D)
        y = self.df[self.response_name].to_numpy() # (N,)
        self.X = X
        self.y = y
        self.ub_ntrain = 2 * self.X.shape[0] # upper bound used to make lgbm determinsitic 
        return 
    
    def make_pipeline(self,
                      learner):
        # reference on using sklearn pipeline https://scikit-learn.org/stable/modules/compose.html#pipeline
        if learner == "lm":
            pipe = Pipeline([('scaler', StandardScaler()), 
                            ('imputer',SimpleImputer()),
                            ('lm', LinearRegression())])
            non_learner_steps = [0,1]
        else:
            assert learner == "lgbm"
            pipe = Pipeline([('scaler', StandardScaler()), 
                         ('imputer',SimpleImputer()),
                         ('lgbm', LGBMRegressor(subsample_for_bin = self.ub_ntrain))])
            non_learner_steps = [0,1]
        return pipe, non_learner_steps

class OneFit_Experiment(Experiment):
    def __init__(self,
                 df, 
                 var_names, 
                 response_name,
                 n_fold,
                 random_seed):
         Experiment.__init__(self,
                            df, 
                            var_names, 
                            response_name,
                            n_fold,
                            random_seed)

    def fit(self,
            learner):
        pipe, _ = self.make_pipeline(learner)
        pipe.fit(self.X, self.y)
        return pipe 

class CV_Experiment(Experiment):

    def __init__(self,
                 df, 
                 var_names, 
                 response_name,
                 n_fold,
                 random_seed):
        Experiment.__init__(self,
                            df, 
                            var_names, 
                            response_name,
                            n_fold,
                            random_seed)
    
    def make_cv_folds(self):
        kf = KFold(n_splits = self.n_fold,
                   shuffle= True,
                   random_state= self.random_seed)
        cv_folds = kf.split(self.X)
        return cv_folds

    def cv_fit(self,
            learner):
        """_summary_

        Args:
            learner (_type_): _description_

        Returns:
            _type_: _description_
        """
        cv_folds = self.make_cv_folds()
        pipe, _ = self.make_pipeline(learner)
        cv_results = cross_validate(pipe, 
                                    X = self.X, 
                                    y = self.y, 
                                    cv = cv_folds,
                                    scoring= ["neg_mean_absolute_error", 
                                              "neg_root_mean_squared_error",
                                              "neg_mean_absolute_percentage_error"],
                                    return_estimator=True,
                                    return_indices = True,
                                    verbose = 1,
                                    n_jobs=4)
        return cv_results
