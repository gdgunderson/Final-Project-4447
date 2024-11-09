'''
This script has functions to merge listings data and geographic tracts data.

The function "merge_listings_and_tracts" should be used to read and create a
GeoPandas geodataframe.

'''
import geopandas as gpd
from read_data.listings import read_listings


def read_tracts_parquet(path: str | None = None) -> gpd.GeoDataFrame:
    '''
    Reads the tracts from the parquet file. The parquet file should contain
    Geospatial data.

    :param path: str. name of the folder containing the parquet file.
    :return: gpd.GeoDataFrame.
    '''
    # if path is not specified
    if path is None:

        # set the path below as the default
        path = '../shapefile_data'

    # the file name
    filename = 'suffolk_ma_gdf.parquet'

    # full path route
    full_path = f'{path}/{filename}'

    # read the parquet into a geodataframe
    gdf = gpd.read_parquet(full_path)

    # return the geodataframe
    return gdf

def merge_listings_and_tracts(
        path_to_tracts: str | None = None,
        path_to_listings: str | None = None
) -> gpd.GeoDataFrame:
    '''
    Merges listings and tracts into a geodataframe.

    :param path_to_tracts: path to folder name containing tracts parquet file
    :param path_to_listings: path to folder name containing the listings JSON files.
    :return: geoDataFrame
    '''
    # if the path to tracts is not specified, then use the one below as the default
    if path_to_tracts is None:
        path_to_tracts = '../shapefile_data'

    # repeat logic with path to listings data
    if path_to_listings is None:
        path_to_listings = '../housing_api/listings'

    # reads listings as a Pandas dataframe
    listings_df = read_listings(path_to_listings)

    # converts the listings dataframe to GeoDataFrame
    listings_gdf = gpd.GeoDataFrame(
        data=listings_df,
        geometry=gpd.points_from_xy(
            listings_df.longitude, listings_df.latitude,
            # epsg:4326 -> WGS 84 World Geodetic System 1984. Source: https://epsg.io/4326
            crs='EPSG:4326'
        )
    ).copy()

    # reads tracts data as a GeoDataFrame
    tracts_gdf = read_tracts_parquet(path_to_tracts)

    # do Spatial Join with GeoPandas
    gdf = listings_gdf.sjoin(tracts_gdf.drop(columns=['latitude', 'intptlat', 'intptlon']), how='left', predicate='within')
    return gdf

if __name__ == "__main__":
    gdf = merge_listings_and_tracts()
    gdf.info()
