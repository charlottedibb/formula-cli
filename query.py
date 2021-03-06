import requests
import argparse
import flag
import pandas as pd
import termtables as tt
from pprint import pprint

df = pd.read_csv('./Countries-List.csv')

parser = argparse.ArgumentParser(description='Get Formula 1 standings.')
parser.add_argument('request', type=str,
                    help="Enter the requested standings, e.g. drivers, constructors")
args = parser.parse_args()


def get_country_code(nationality: str):
    return df['ISO 3166 Code'][df['Demonym'] == nationality].values[0]


def ergast_retrieve(api_endpoint: str):
    url = f'https://ergast.com/api/f1/{api_endpoint}.json'
    response = requests.get(url).json()
    return response['MRData']


def format_driver_standings(driver_standings: list):
    drivers = driver_standings['StandingsTable']['StandingsLists'][0]['DriverStandings']
    driver_data = []
    for driver in drivers:
        country_code = get_country_code(driver['Driver']['nationality'])
        emoji = flag.flag(country_code)
        initial = driver['Driver']['givenName'][0]
        familyName = driver['Driver']['familyName']
        name_and_flag = f'{emoji}  {initial}. {familyName}'
        driver_data.append(
            [driver['position'], name_and_flag, driver['Constructors'][0]['name'], driver['points']])
    return driver_data


def format_constructor_standings(constructor_standings: list):
    constructors = constructor_standings['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    constructor_data = []
    for constructor in constructors:
        country_code = get_country_code(
            constructor['Constructor']['nationality'])
        emoji = flag.flag(country_code)
        constructor_data.append([constructor['position'], emoji + "  " +
                                constructor['Constructor']['name'], constructor['points']])
    return constructor_data


if args.request == 'drivers':
    driver_standings = ergast_retrieve('current/driverStandings')

    data = format_driver_standings(driver_standings)

    header = ["Pos", "Driver", "", "Points"]

    tt.print(
        data=data,
        header=header,
        style=tt.styles.booktabs,
        alignment="lllr"
    )

if args.request == 'constructors':
    constructor_standings = ergast_retrieve('current/constructorStandings')

    data = format_constructor_standings(constructor_standings)

    header = ["Pos", "Constructor", "Points"]

    tt.print(
        data=data,
        header=header,
        style=tt.styles.booktabs,
        alignment="llr"
    )
