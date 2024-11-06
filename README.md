# Final-Project-4447
Data Science Tools 1 Final Project - Victor Martinez and Grayson Gunderson

Abstract:
Home prices in the US have outpaced inflation for the past 60 years. The median home price in the US is over 400,000 - approximately 7 times the US median annual income of $60,000. As more and more Americans have been priced out of the housing market, we are interested in understanding what factors drive home price in Suffolk County, MA (Boston, Massachusetts). The goal of this project is to discover the relationship between housing characterics, geographical features, and socioeconomic features on housing prices in Suffolk County. We hope to uncover patterns/trends in the data to learn more about the housing crisis. Ideally, we would like to provide prospective homebuyers that have been priced out of the housing market with information that could improve their chances of being able to afford a home in the future.

Data Collection:
The housing price data was collected with an API service from rentcast.io (https://www.rentcast.io). ***Victor to provide short explanation.****
The Socio-Economic and geographic was collected from the US Census Bureau (https://www.census.gov/). Three Census Data files (Employment Characteristics, Financial Characteristics, Total Population)  were downloaded and imported to the Census_Data_Cleaning_Final.ipynb file. The Census Data contained Socioeconomic Data for Suffolk County, Massachussets seperated by Census Tract - a subdivision of a county. This data was transposed, thoroughly cleaned/filtered, re-organized, and finally combined into a single Census Data Frame that was output as a parquet file. Some feauture engineering was performed during this stage. In the final stage of our Data collection process, the Shapefile, Listings data frame, and Census data frame was merged into a single data frame on the feature 'Tract'. This merged dataframe was imported into a new jupyter notebook for analysis and modeling via a python script 'read_listings_tracts_census.py'.

EDA/Feature Engineering: 
Dummy Variables were created for categorical variables containing zip codes, property types, listing types, and city names. A new feature named 'density' was added to the data frame by dividing the 'tract area' by the 'total population' of each tract. This feature was created in an attempt to create a variable that had correlation with supply of housing - a data point we were not able to retrieve during our data collection phase.

Distribution analysis was conducted on each feature to determine the appropriate method of normalization. All features requiring scaling were determined to have non-normal distributions based on the results of the Shapiro-Wilk test. Numerical features requiring normalization were then scaled using min-max scaling. The dummy variables and target variable 'price' were excluded from min-max scaling.

Correlation analysis was performed, exposing significant multicollinearity in the data. In an attempt to reduce Multicollinearity, features belonging to feature pairs with absolute correlation values greater than .5 were removed. The feature with the lower correlation value with the target-variable 'price' was removed from each high-correlation feature pair. Finally, each remaining feature was sorted by their absolute correlation with price, and all features with correlation values < .10 were removed from the dataframe. In total, 55 features were removed during this phase and the data frame used for Machine Learning contained 10 features.

Modeling:

Results:
