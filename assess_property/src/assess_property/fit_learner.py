
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

from assess_property.global_variables import LU_LIST, YR_TO_NAME, ZIPCODE_FILLNA, DATA_DIR

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
    
    def make_cv_folds(self):
        kf = KFold(n_splits = self.n_fold,
                   shuffle= True,
                   random_state= self.random_seed)
        cv_folds = kf.split(self.X)
        return cv_folds

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
                                    verbose = 1,
                                    n_jobs=4)
        return cv_results
    
    def fit(self,
            learner,
            fold_idx):
        """_summary_

        Args:
            fold_idx (_type_): _description_
        """
        cv_folds = list(self.make_cv_folds())
        train_indices, test_indices = cv_folds[fold_idx]
        pipe, non_learner_steps = self.make_pipeline(learner)

        xtrain, ytrain = self.X[train_indices], self.y[train_indices]
        xtest, ytest = self.X[test_indices], self.y[test_indices]

        pipe.fit(xtrain, ytrain)
        ypred = pipe.predict(xtest)

        datadict = {"xtrain": xtrain,"ytrain": ytrain,
                    "xtest": xtest, "ytest": ytest}
        
        modeldict = {"pipe": pipe, 
                     "ypred": ypred}
        
        return datadict, modeldict  
