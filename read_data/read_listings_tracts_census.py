import pandas as pd
from read_data.listings_and_tracts import merge_listings_and_tracts


def read_listings_tracts_census(
        path_to_tracts: str | None = None,
        path_to_listings: str | None = None,
        path_to_census: str | None = None
):
    '''
    This function puts together all data sources into a single DataFrame

    :param path_to_tracts: str | None. defaults to None
    :param path_to_listings: str | None. defaults to None
    :param path_to_census: str | None. defaults to None
    :return: df (pandas.DataFrame)
    '''
    # if the path to tracts is not specified, then use the one below as the default
    if path_to_tracts is None:
        path_to_tracts = '../shapefile_data'

    # repeat logic with path to listings data
    if path_to_listings is None:
        path_to_listings = '../housing_api/listings'

    if path_to_census is None:
        path_to_census = '../Census_Data'

    # call census filename. This file contains socio-economic data
    census_filename = 'df_census.parquet'

    # read the census file
    census_df = pd.read_parquet(f'{path_to_census}/{census_filename}')

    # read and load listings and tracts into a dataframe
    listings_tracts_df = merge_listings_and_tracts(
        path_to_tracts=path_to_tracts,
        path_to_listings=path_to_listings
    )

    # rename tract columns from the census socio-economic dataset
    census_df = census_df.rename({'Tract': 'tract_name'}, axis=1)

    # remove unwanted columns from listings_and_tracts dataframe
    listings_tracts_df = listings_tracts_df.drop(
        columns=[
            'mlsName',
            'mlsNumber',
            'listingAgent',
            'history',
            'hoa',
            'builder',
            'mtfcc',
            'funcstat',
            'aland',
            'awater'
        ]
    )

    # merge all datasets
    df = pd.merge(
        left=listings_tracts_df,
        right=census_df,
        how='left',
        on='tract_name'
    )

    # make dictionary to rename some columns
    rename_dict = {
        'Total Population': 'total_pop',
        'Occupied housing units': 'occupied_housing_units',
        'Median monthly housing cost': 'median_monthly_housing_cost',
        'Median household income': 'median_household_income',
        'Median household income below 100k (percent occupied housing units)': 'median_housing_income_below_100k',
        'Median household income 100k to 149k (percent occupied housing units)': 'median_housing_income_100k_149k',
        'Median household income 150k and above (percent occupied housing units)': 'median_housing_income_150k_above',
        'At or above the poverty level (Unemployment Rate)': 'at_or_above_pov_level_unemployment_r',
        'Population 25 to 64 years (Unemployment Rate)': 'pop_25_to_64_yrs_unemployment_r',
        'Bachelors degree or higher (Unemployment Rate)': 'bach_degree_unemployment_r'
    }

    # rename the columns
    df = df.rename(rename_dict, axis=1)

    # remove records where counties are Norfolk and Middlesex
    df = df[df['county'] != 'Norfolk']
    df = df[df['county'] != 'Middlesex']

    return df


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df = read_listings_tracts_census()

    df.info()
