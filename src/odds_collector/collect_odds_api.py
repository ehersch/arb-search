from abc import ABC, abstractmethod

from pydantic import BaseModel
import json
import requests
from collections import defaultdict


class MatchupKeySchema(BaseModel):
    away_team: str
    home_team: str
    game_time: int


class BooksSchema(BaseModel):
    books_list_element: tuple[str, list[float]]


def hashable(schema: MatchupKeySchema):
    """
    Hashes a MatchupKeySchema to a tuple
    """
    return (schema.away_team, schema.home_team, schema.game_time)


class OddsCollectionInterface(ABC):
    def __init__(self):
        return

    # @abstractmethod
    # def fetch_data(self, write_to_path):
    #     pass

    # @abstractmethod
    # def process_data(self):
    #     pass

    @abstractmethod
    def retrieve_data(self):
        pass


class OddsAPICollection(OddsCollectionInterface):
    def __init__(self):
        super().__init__()

    def write_to(self, filename):
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
        """ print()
          print(
              "Successfully got {} events".format(len(odds_json["data"])),
              "Here's the first event:",
          )
          print(odds_json["data"][0])"""
        
    def parse_json(self, filename):
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
        matchups = defaultdict(list[BooksSchema])

        # Process each game in the odds data
        for i in range(num_games):
            team1 = data["data"][i]["teams"][0]
            team2 = data["data"][i]["teams"][1]
            home_team = data["data"][i]["home_team"]
            is_ordered = home_team == team2

            time = data["data"][i]["commence_time"]
            if is_ordered:
                key = MatchupKeySchema(away_team = team1, home_team = team2, game_time = time)
            else:
                key = MatchupKeySchema(away_team = team2, home_team = team1, game_time = time)
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
            key = hashable(key)
            matchups[key] = lst
        return matchups

    def retrieve_data(self, file_to_write_to):
         self.write_to(file_to_write_to)
         odds_dict = self.parse_json(file_to_write_to)
         return odds_dict