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
              and the value is a list of tuples. Note, we go by (away, home).
              Each tuple in the list contains:
                - site (str): The name of the betting site.
                - odds (list): A list of odds for the two teams, where the first element corresponds to the
                  home team and the second element corresponds to the away team.

    The function reads odds data from the specified JSON file, processes it to extract team names, game time,
    and odds from various sites, and organizes this information into a dictionary. The key in the dictionary is
    a tuple of the form (away, home, time), and the value is a list of tuples where each tuple contains a site
    name and a list of odds.

    Example:
        matchups = main("odds1.json")
    """
    # Open and load the JSON file containing odds data
    with open(filename) as f:
        data = json.load(f)

    num_games = len(data["data"])
    matchups = defaultdict(list)

    # Process each game in the odds data
    for i in range(num_games):
        team1 = data["data"][i]["teams"][0]
        team2 = data["data"][i]["teams"][1]
        home_team = data["data"][i]["home_team"]
        is_ordered = home_team == team1

        time = data["data"][i]["commence_time"]
        if is_ordered:
            key = (team1, team2, time)
        else:
            key = (team2, team1, time)
        lst = []
        num_sites = data["data"][i]["sites_count"]

        # Extract odds from each site
        for j in range(num_sites):
            site = data["data"][i]["sites"][j]["site_key"]
            odds1, odds2 = data["data"][i]["sites"][j]["odds"]["h2h"]
            if is_ordered:
                odds = [odds1, odds2]
            else:
                odds = [odds2, odds1]
            lst.append((site, odds))

        # Add the list of odds for the matchup to the dictionary
        matchups[key] = lst

    return matchups


if __name__ == "__main__":
    main("odds1.json")
