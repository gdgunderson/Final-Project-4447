import logging
import os
import requests
import time
import json
from datetime import date
from dotenv import load_dotenv
from locations_for_api import LOCATION_DICTIONARIES


def find_listings(
        location_data: dict
):
    '''
    API client to find property listings from Rentcast.io. This client makes 1 API call.
    An API call finds up to 500 property listings within a 1 mile radius.

    :param location_data: dictionary of location.
    :return:
    '''
    # name of location
    name: str = location_data['name']
    latitude: float = location_data['latitude']
    longitude: float = location_data['longitude']
    # status of the properties. example: Active
    status: str = location_data['status']

    # get API key from .env file
    api_key = os.getenv('rentcast_api_key')

    # setup headers
    headers = {
        'accept': 'application/json',
        'X-api-key': api_key
    }

    # if the bathrooms number is specified, use the parameters dictionary below.
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': 1.0,  # miles
        'status': status,
        'limit': '500',
        'propertyType': 'for-sale'
    }

    # sleeping 1 seconds before making API call
    seconds = 1
    logging.info('sleeping: %s ...', seconds)
    time.sleep(seconds)

    logging.info('Requesting Listings to Rentcast API for %s...',
                 name)

    # make GET request
    response = requests.get(url='https://api.rentcast.io/v1/listings/sale',
                            params=params,
                            headers=headers
                            )

    # get JSON object from response
    response_json = response.json()

    # name of folder to store the raw json files
    folder = 'listings'

    if not os.path.exists(folder):
        os.makedirs(folder)

    # get string value of today's date
    date_str = str(date.today())

    # setting up filename for the JSON file
    filename = f'{name}_{date_str}_{status.upper()}.json'
    path_output = f'{folder}/{filename}'

    # save the dictionary into a JSON file
    with open(path_output, 'w', encoding='utf-8') as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)
        logging.info('Downloaded to %s', path_output)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    for location in LOCATION_DICTIONARIES:
        find_listings(location_data=location)

