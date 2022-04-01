import requests
import argparse
import termtables as tt
from pprint import pprint

parser = argparse.ArgumentParser(description='Get Formula 1 standings.')
parser.add_argument('request', type=str,
                    help="Enter the requested info, e.g. driver-standings")
args = parser.parse_args()
print(args.request)


def ergast_retrieve(api_endpoint: str):
    url = f'https://ergast.com/api/f1/{api_endpoint}.json'
    response = requests.get(url).json()
    return response


if args.request == 'driver-standings':
    result = ergast_retrieve('current/driverStandings')
    pprint(result)
