"""
Module to parse and organize baseball odds data from a JSON file.

This module contains a function to parse baseball odds data from a JSON file,
reformat it into a more manageable structure, and return it as a dictionary.
The resulting dictionary is keyed by matchups (team names and game time) and
contains a list of sites and their associated odds.

Dependencies:
    json: For handling JSON data.
    collections.defaultdict: For creating a dictionary with default list values.

Functions:
    main(filename): Parses the JSON file containing baseball odds data and returns a formatted dictionary.

Example usage:
    Call the `main` function with the filename of the JSON file to get the formatted data:
        matchups = main("odds1.json")
"""

import json
from collections import defaultdict


def main(filename):
    """
    Parses baseball odds data from a JSON file and returns a formatted dictionary.

    Args:
        filename (str): The path to the JSON file containing the odds data.

    Returns:
        dict: A dictionary where the key is a tuple containing the matchup (team names and game time)
              and the value is a list of tuples. Each tuple in the list contains:
                - site (str): The name of the betting site.
                - odds (list): A list of odds for the two teams, where the first element corresponds to the first
                  alphabetical team and the second element corresponds to the second team.

    The function reads odds data from the specified JSON file, processes it to extract team names, game time,
    and odds from various sites, and organizes this information into a dictionary. The key in the dictionary is
    a tuple of the form (team1, team2, time), and the value is a list of tuples where each tuple contains a site
    name and a list of odds.

    Example:
        matchups = main("odds1.json")
    """
    # Open and load the JSON file containing odds data
    with open(filename) as f:
        data = json.load(f)

    # Open and load the JSON file containing team names (for potential use)
    with open("data/teams.json") as g:
        teams = json.load(g)

    num_games = len(data["data"])
    matchups = defaultdict(list)

    # Process each game in the odds data
    for i in range(num_games):
        team1 = data["data"][i]["teams"][0]
        team2 = data["data"][i]["teams"][1]
        time = data["data"][i]["commence_time"]
        key = (team1, team2, time)
        lst = []
        num_sites = data["data"][i]["sites_count"]

        # Extract odds from each site
        for j in range(num_sites):
            site = data["data"][i]["sites"][j]["site_key"]
            odds = data["data"][i]["sites"][j]["odds"]["h2h"]
            lst.append((site, odds))

        # Add the list of odds for the matchup to the dictionary
        matchups[key] = lst

    return matchups


if __name__ == "__main__":
    main("odds1.json")
