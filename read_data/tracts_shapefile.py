import logging
import os
import geopandas as gpd
import pandas as pd

def read_shapefile_save_to_parquet(
      path: str
) -> gpd.GeoDataFrame:
    '''
    Read shapefile and save to parquet file.
    :param path: str. path to reach shapefile
    :return: geodataframe object.
    '''
    # read shapefile
    gdf = gpd.read_file(path)

    # filtering down to Suffolk County, MA
    county_gdf = gdf[gdf['COUNTYFP'] == '025'].copy()

    # rename tract column
    county_gdf = county_gdf.rename({'NAME': 'tract_name'}, axis=1)

    # changing the CRS to EPSG:4326, which puts coordinates to degrees
    county_gdf.to_crs(epsg=4326, inplace=True)

    # lower casing all column names
    cols = county_gdf.columns.tolist()
    lower_cols = [col.lower() for col in cols]
    county_gdf.columns = cols

    # explode geodataframe
    county_gdf = county_gdf.explode(column='geometry', ignore_index=True, index_parts=False).copy()

    if county_gdf[county_gdf.duplicated(subset='geometry')].shape[0] > 0:
        raise ValueError('GeoDataFrame has duplicated geometry values')

    # compute latitude and longitude of polygon centroids
    county_gdf['latitude'] = county_gdf['geometry'].apply(lambda x: x.centroid.y)
    county_gdf['latitude'] = county_gdf['geometry'].apply(lambda x: x.centroid.x)

    # compute area of tract. unit of measurement in meters
    # source: https://epsg.io/26986
    gdf_epsg_26986 = county_gdf.to_crs(epsg=26986).copy()

    # creates new column area is computed in kilometers
    county_gdf['area'] = gdf_epsg_26986['geometry'].apply(lambda x: x.area / 10**6)

    # store data to parquet file
    folder = '../shapefile_data'
    if not os.path.exists(folder):
        os.makedirs('../shapefile_data')
    path = f'{folder}/suffolk_ma_gdf.parquet'

    # on terminal:
    # $ pip install pyarrow
    # that will allow to store to parquet file
    county_gdf.to_parquet(path=path)
    logging.info('Parquet saved to %s', path)

    return county_gdf

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = read_shapefile_save_to_parquet(path="../shapefile_data/tl_2022_25_tract/tl_2022_25_tract.shp")
    data.info()