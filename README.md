# Boston Parcel Price Prediction
This repo builds a supervised learning model, evaluate accuracy and visualize feature importance, for the task of predicting Boston parcel prices in terms of a parcel's physical attributes.

# Business Use Cases
Accuracte predictions of a parcel's total value is important to:
- The City: 
    - to determine the tax 
    each year, there are about 160k parcels to price. a good prediction system can reduce the time spent by city officials. 
For owners/real estate companies
- which property is improving in value, which is not? 
    + a couple wants to buy a place, and wants to optimize for future value
- what is the impact of features/renovations on the total value? 
    + among a set of possible renovations, which one gives the most value?

# Methodology

## Deciding on Relevant Features 
Based on https://data.boston.gov/dataset/property-assessment/resource/4973f23e-859e-4190-b308-8223c246147e,
we propose the following list of features for building predictions the parcel's total value are:
- living area
- year built
- year since remodeling

Future work should include a) number of rooms and b) zipcode as relevant predictive features. 

## Exploratory Data Analysis 

[Basic visualization of the features and the response](assess_property/notebooks/visualize_data.ipynb)

## Building and Evaluating Predictive Model
[Cross-validation shows that boosting models have higher predictive accuracy compared to linear models](assess_property/notebooks/cross_validate.ipynb)

## Analyze Feature Importance
[SHAP feature importance plots reveal that LIVING_AREA is the biggest determinant of TOTAL_VALUE](assess_property/notebooks/visualize_feature_importance.ipynb)