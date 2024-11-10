# Final-Project-4447
Data Science Tools 1 Final Project - Victor Cairo and Grayson Gunderson

## Abstract:  
Home prices in the US have outpaced inflation for the past 60 years. The median home price in the US is over 400,000 - approximately 7 times the US median annual income of $60,000. As more and more Americans have been priced out of the housing market, we are interested in understanding what factors drive home price in Suffolk County, MA (Boston, Massachusetts). The goal of this project is to discover the relationship between housing characterics, geographical features, and socioeconomic features on housing prices in Suffolk County. We hope to uncover patterns/trends in the data to learn more about the housing crisis. Ideally, we would like to provide prospective homebuyers that have been priced out of the housing market with information that could improve their chances of being able to afford a home in the future.

## Data Collection:  
The housing price data was collected with an API service from rentcast.io (https://www.rentcast.io). The Rentcast.io API is a paid API service that offers millions of housing listings records in the US. From this API we collected features such as the home price, bathroom count, bedroom count, lot size, square footage, status, latitude and longitude, address, etc.   
The Socio-Economic and geographic was collected from the US Census Bureau (https://www.census.gov/). Three Census Data files (Employment Characteristics, Financial Characteristics, Total Population)  were downloaded and imported to the Census_Data_Cleaning_Final.ipynb file. The Census Data contained Socioeconomic Data for Suffolk County, Massachussets seperated by Census Tract - a subdivision of a county. This data was transposed, thoroughly cleaned/filtered, re-organized, and finally combined into a single Census Data Frame that was output as a parquet file. Some feauture engineering was performed during this stage. In the final stage of our Data collection process, the Shapefile, Listings data frame, and Census data frame was merged into a single data frame on the feature 'Tract'. This merged dataframe was imported into a new jupyter notebook for analysis and modeling via a python script 'read_listings_tracts_census.py'.
Geospatial data from US Census: Tracts and counties shapefile of MA. (https://www2.census.gov/geo/tiger/TIGER2022/TRACT/). The US Census has a repository of shapefiles that contain geospatial information of geo-political areas in the US. We loaded Massachussetts' shapefile to map the housing listings to their respective US Census tracts. We merged the data with a spatial join function from GeoPandas library. 

### Scripts for Data Collection
Our github repository contains additional scripts that were used to collect the data. We decided to separate this process from the Jupyter notebook to make the content from the notebook clearer and appear less cluttered. 

The scripts are located at the following folders: "Census_Data", "housing_api", "read_data", and "shapefile_data". The "Census_Data" folder contains the code that processes the socio-economic data from the US Census. The housing_api folder contains the API client we constructed to perfrom the API calls to RentCast.io and get the housing listings. In the "housing_api" folder we store the raw data collected from the API. The raw data is presented in Json files. The "shapefile_data" contains the parquet file that is ingested from the scripts that are located at "read_data" folder. Lastly the "read_data" folder contains utility functions to read and merge the data that is used for Machine Learning and Analysis. 

## EDA/Feature Engineering:  
Dummy Variables were created for categorical variables containing zip codes, property types, listing types, and city names. A new feature named 'density' was added to the data frame by dividing the 'tract area' by the 'total population' of each tract. This feature was created in an attempt to create a variable that had correlation with supply of housing - a data point we were not able to retrieve during our data collection phase.

Distribution analysis was conducted on each feature to determine the appropriate method of normalization. All features requiring scaling were determined to have non-normal distributions based on the results of the Shapiro-Wilk test. Numerical features requiring normalization were then scaled using min-max scaling. The dummy variables and target variable 'price' were excluded from min-max scaling.

Correlation analysis was performed, exposing significant multicollinearity in the data. In an attempt to reduce Multicollinearity, features belonging to feature pairs with absolute correlation values greater than .5 were removed. The feature with the lower correlation value with the target-variable 'price' was removed from each high-correlation feature pair. Finally, each remaining feature was sorted by their absolute correlation with price, and all features with correlation values < .10 were removed from the dataframe. In total, 55 features were removed during this phase and the data frame used for Machine Learning contained 10 features.

## Modeling:  
Machine Learning Models Tested:
1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Gradient Boosting Regressor

Initial modeling results unimpressive and showed severe signs of overfitting. After unimpressive initial results, IQR was employed to remove the 80 most extreme observations for home price. GridSearchCV was employed to test multiple sets of hyperparameters, returning the best set and perform cross-validation to evalutate model performance - reducing the risk of over/under-fitting.

### Results:  
After outlier removal/hyperparameter tuning, RMSE and mean residuals were significantly reduced in each model. 

Test RMSE
OLS: 868,696.38 USD
Tree: 733,867.41 USD
Random Forest: 641,707.12 USD
Gradient Boosting: 616,504.17 USD

Test Mean Residuals
OLS: -4,852.56 USD
Tree: -6,424.10 USD
Random Forest: 564.67 USD
Gradient Boosting: -9,522.15 USD

The model with the lowest RMSE was the Gradient Boosting Regressor and was therefore chosen as the final model. Top 3 most important features of final model (in order): square footage, latitude, median monthly housing cost.


## Conclusion:  
Large Variations in housing price, even among homes located in the same county, present unique challenges when attempting to predict housing prices.

We believe that some of this information will be useful to prospective home-buyers, however, much of the results revealed by our models revealed commonly known information. It is self-evident that larger houses with more square footage are more expensive, and that areas with higher median monthly housing cost, have more expensive housing. Some of the more interesting results were based on location, days on market, and particular zip codes. These are characteristics that are may be less known to the public, and could actually provide some valuable information, although these features do not have as strong an impact on price as square footage.

Although our results were not as transformative as we had hoped, any insights that give homebuyers a slight advantage in the market are valuable. To truly understand the nuances of housing prices and find more affordable options, homebuyers should take a holistic view of the housing market. Prospective buyers should create a thorough list of the housing characteristics that are less important to them. By identifying these areas where they are willing to compromise, they can make smaller sacrifices that collectively lead to substantial cost savings, potentially making their first home purchase possible.
