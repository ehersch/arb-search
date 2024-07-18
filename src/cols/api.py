from oddsapi import OddsApiClient
from asyncio import gather
import json
import requests

# The intent of this file is to get baseball odds from https://api.the-odds-api.com/v3/odds
#  and save them as a json file.
# Once you make a json, make sure to CHANGE THE NAME of the next one.

# API_KEY = "***"

odds_response = requests.get(
    "https://api.the-odds-api.com/v3/odds",
    params={
        "api_key": API_KEY,
        "sport": "baseball_mlb",
        "region": "us",  # uk | us | eu | au
        "mkt": "h2h",  # h2h | spreads | totals
        "oddsFormat": "american",
    },
)

filename = "odds1.json"
odds_json = odds_response.json()

# Write the dictionary to the JSON file
with open(filename, "w") as file:
    json.dump(odds_json, file, indent=4)

odds_json = json.loads(odds_response)

if not odds_json["success"]:
    print("There was a problem with the odds request:", odds_json["msg"])

else:
    # odds_json['data'] contains a list of live and
    #   upcoming events and odds for different bookmakers.
    # Events are ordered by start time (live events are first)
    print()
    print(
        "Successfully got {} events".format(len(odds_json["data"])),
        "Here's the first event:",
    )
    print(odds_json["data"][0])
