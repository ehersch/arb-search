"""
Module to fetch and save baseball odds data from an API.

This module contains a function to request baseball odds data from the Odds API,
parse the JSON response, and save it to a file. The function also includes basic
error handling and prints the number of events retrieved and details of the first event.

Dependencies:
    requests: For making HTTP requests to the Odds API.
    json: For handling JSON data.

Functions:
    write_to(filename): Fetches baseball odds data from the Odds API and saves it to a JSON file.

Example usage:
    Call the `write_to` function with a filename to fetch and save the data:
        write_to("odds1.json")
"""

from asyncio import gather
import json
import requests


def write_to(filename):
    """
    Fetches baseball odds data from the Odds API and saves it to a JSON file.

    Args:
        filename (str): The name of the file where the JSON data will be saved.

    This function sends a GET request to the Odds API to retrieve baseball odds
    for MLB games. It then writes the data to a JSON file with the specified
    filename. After saving the file, it prints the number of events retrieved
    and details of the first event if the request was successful. If there is an
    issue with the request, an error message is printed.

    Note:
        - You need to replace the `API_KEY` placeholder with a valid API key.
        - Make sure to change the filename for each new request to avoid overwriting previous files.

    Example:
        write_to("odds1.json")
    """
    # API_KEY = "***"  # Replace with your actual API key

    odds_response = requests.get(
        "https://api.the-odds-api.com/v3/odds",
        params={
            "api_key": API_KEY,
            "sport": "baseball_mlb",
            "region": "us",  # Options: uk | us | eu | au
            "mkt": "h2h",  # Options: h2h | spreads | totals
            "oddsFormat": "american",
        },
    )

    odds_json = odds_response.json()

    # Write the dictionary to the JSON file
    with open(filename, "w") as file:
        json.dump(odds_json, file, indent=4)

    # Check if the response was successful
    if not odds_json["success"]:
        print("There was a problem with the odds request:", odds_json["msg"])
    else:
        # Print the number of events and details of the first event
        print()
        print(
            "Successfully got {} events".format(len(odds_json["data"])),
            "Here's the first event:",
        )
        print(odds_json["data"][0])


if __name__ == "__main__":
    write_to("odds1.json")
