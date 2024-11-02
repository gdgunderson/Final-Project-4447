from datetime import date
import pandas as pd
import json
import os

def read_listings(
        path_to_files: str,
        date_created: date = date(2024, 10, 9)
) -> pd.DataFrame:
    '''
    Read the housing listings from raw json files and return a DataFrame
    :param path_to_files: str. path to find the files
    :param date_created: date created of files. datetime.date object
    :return: pandas dataframe with housing listings
    '''
    date_str = str(date_created)

    files = os.listdir(path_to_files)

    # make list to store file names
    record_df_list = []

    # select active properties from the input date
    files = [file for file in files if date_str in file and "ACTIVE" in file]

    # for i in the range of the size of the list of files from the folder
    for i in range(len(files)):
        file = files[i]

        # make file path
        path_file = f'{path_to_files}/{file}'

        # read the JSON file
        with open(path_file, 'r') as f:

            # load the data into a Python dictionary
            data = json.load(f)

        # for each record in the json file
        for record in data:
            # make a list of the values from the dictionary.
            # ensure each value is within a list
            values = [[value] for value in list(record.values())]

            # make a new dictionary of the keys and values
            record = dict(zip(list(record.keys()), values))

            # use that new dictionary to make a Pandas DataFrame
            record_df = pd.DataFrame(data=record)

            # append the DataFrame into the list of dataframes
            record_df_list.append(record_df)

    # concatenate all dataframes into a single dataframe
    df = pd.concat(record_df_list, axis=0)

    df = df.reset_index(drop=True)

    # basic pre-processing
    df['createdDate'] = pd.to_datetime(df['createdDate'])
    df['lastSeenDate'] = pd.to_datetime(df['lastSeenDate'])
    df = df.drop_duplicates(subset=['id'])

    # return dataframe
    return df

if __name__ == '__main__':
    path_to_files = '../data_temp'
    listings_df = read_listings(path_to_files=path_to_files)

    listings_df.info()
    print(listings_df[['createdDate', 'lastSeenDate']].head())