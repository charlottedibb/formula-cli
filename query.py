import requests
import argparse



def ergast_retrieve(api_endpoint: str):
  url = f'https://ergast.com/api/f1/{api_endpoint}.json'
  response = requests.get(url).json()
  return response

result = ergast_retrieve('current/driverStandings')

print(result)
