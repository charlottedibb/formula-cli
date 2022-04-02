import requests
import argparse
import flag
import pandas as pd
import termtables as tt
from pprint import pprint

df = pd.read_csv('./Countries-List.csv')

parser = argparse.ArgumentParser(description='Get Formula 1 standings.')
parser.add_argument('request', type=str,
                    help="Enter the requested info, e.g. driver-standings")
args = parser.parse_args()

def get_country_code(nationality: str):
    return df['ISO 3166 Code'][df['Demonym'] == nationality].values[0]

def ergast_retrieve(api_endpoint: str):
    url = f'https://ergast.com/api/f1/{api_endpoint}.json'
    response = requests.get(url).json()
    return response['MRData']


if args.request == 'driver-standings':
    result = ergast_retrieve('current/driverStandings')
    drivers = result['StandingsTable']['StandingsLists'][0]['DriverStandings']
    driver_data = []
    for driver in drivers:
        driver_data.append(
            [driver['position'], driver['Driver']['code'], driver['points']])
    pprint(driver_data)
