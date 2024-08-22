import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from webpage_loader import load_page_source


CONDITIONS_FILENAME = "espn_game_states.json"
GAME_STATE_KEY = "game_time_class_name"
LIVE = "live"
PENDING = "pending"
COMPLETED = "completed"


MLB_TEAM_NAMES_MAP = {
    "guardians": "Cleveland Guardians",
    "yankees": "New York Yankees",
    "red sox": "Boston Red Sox",
    "blue jays": "Toronto Blue Jays",
    "orioles": "Baltimore Orioles",
    "rays": "Tampa Bay Rays",
    "white sox": "Chicago White Sox",
    "tigers": "Detroit Tigers",
    "royals": "Kansas City Royals",
    "twins": "Minnesota Twins",
    "astros": "Houston Astros",
    "athletics": "Oakland Athletics",
    "mariners": "Seattle Mariners",
    "angels": "Los Angeles Angels",
    "rangers": "Texas Rangers",
    "mets": "New York Mets",
    "braves": "Atlanta Braves",
    "phillies": "Philadelphia Phillies",
    "marlins": "Miami Marlins",
    "nationals": "Washington Nationals",
    "cubs": "Chicago Cubs",
    "brewers": "Milwaukee Brewers",
    "cardinals": "St. Louis Cardinals",
    "pirates": "Pittsburgh Pirates",
    "reds": "Cincinnati Reds",
    "dodgers": "Los Angeles Dodgers",
    "giants": "San Francisco Giants",
    "padres": "San Diego Padres",
    "rockies": "Colorado Rockies",
    "diamondbacks": "Arizona Diamondbacks" 
}


def load_conditions(filename):
    with open(filename, "r") as condition_file:
        return json.load(condition_file)


def identify_page_state(condition_mapping, soup):
    class_name = condition_mapping[GAME_STATE_KEY]
    element = soup.select(f".{class_name}")[0]
    condition = element.text.lower()

    if "final" in condition:
        return COMPLETED
    elif "pm" in condition or "am" in condition:
        return PENDING
    else:
        return LIVE
    

class GameAnalyser(ABC):
    def __init__(self, soup, args, condition_mapping):
        self.soup = soup
        self.args = args
        self.condition_mapping = condition_mapping

    def find_condition(self):
        my_condition = {}
        for condition in self.condition_mapping["mlb_game_conditions"]:
            if condition["state"] == self.STATE:
                my_condition = condition
        return my_condition
    
    # def get_team_names(self):
    #     team_names_class = "ScoreCell__TeamName"
    #     team_names = self.soup.select(f".{team_names_class}")
    #     team_names = [team_names[0].text.lower(), team_names[1].text.lower()]
    #     return team_names
    
    def get_team_names(self, retry=1):
        team_names_class = "ScoreCell__TeamName"
        
        for _ in range(retry):
            team_names = self.soup.select(f".{team_names_class}")
            
            if len(team_names) < 2:
                continue  # In case the expected elements aren't found, retry

            team_names = [team_names[0].text.lower(), team_names[1].text.lower()]
            
            # Check if both team names are in the MLB_TEAM_NAMES_MAP
            if team_names[0] in MLB_TEAM_NAMES_MAP and team_names[1] in MLB_TEAM_NAMES_MAP:
                return team_names  # Return if both team names are found in the map
        
        # If we exhaust retries or the team names aren't found in the map, return empty strings
        return ["", ""]

    @classmethod
    def create_payload(cls, away_team, home_team, at_matchup_prediction, ht_matchup_prediction):
        return {
           cls.STATE: {
                "away": {
                    "team_name": away_team,
                    "matchup_prediction": at_matchup_prediction,
                },
                "home": {
                    "team_name": home_team,
                    "matchup_prediction": ht_matchup_prediction
                }
            } 
        }


    @abstractmethod
    def is_complete(self) -> bool:
        pass

    @abstractmethod
    def process(self):
        pass


class LiveGameAnalyser(GameAnalyser):
    STATE = LIVE

    def process(self):
        my_condition = self.find_condition()
        team_names = self.get_team_names()
        
        class_name = my_condition["wait_class_name"]
        target_nodes = self.soup.select(f".{class_name}")
        
        # Get matchup prediciton as a float
        matchup_prediction = target_nodes[0].text
        matchup_prediction = matchup_prediction.replace("%", " ").split(" ")
        matchup_prediction = float(matchup_prediction[0])

        # Get the team who the matchup prediction is for 
        img_for_team = self.soup.select(f".{class_name} img")[0]
        for_team = img_for_team["alt"] # win probability for team `for_team`
        # Grab team names from matchup prediction graph
        team_names_again = self._get_alt_team_names()
        for_team_key = self._find_key(for_team)

        payload = {
            "away_team": team_names_again[0],
            "home_team": team_names_again[1],
            "matchup_prediction_away": 0.,
            "matchup_prediction_home": 0.
        }
        # Matchup prediction is for the home team
        if for_team_key == team_names_again[0]:
            payload["matchup_prediction_away"] = str(matchup_prediction)
            payload["matchup_prediction_home"] = str(100. - matchup_prediction)
        else:
            payload["matchup_prediction_home"] = str(matchup_prediction)
            payload["matchup_prediction_away"] = str(100. - matchup_prediction)

        matchup_payload = self.create_payload(
            payload["away_team"],
            payload["home_team"],
            payload["matchup_prediction_away"],
            payload["matchup_prediction_home"]
        )
        return matchup_payload
    
    def _find_key(self, for_team):
        for (key, value) in MLB_TEAM_NAMES_MAP.items():
            if value == for_team:
                return key

    def _get_alt_team_names(self):
        class_name = "CustomLegend__TeamName"
        team_names = self.soup.select(f".{class_name}")
        team_names = [team_names[0].text.lower(), team_names[1].text.lower()]
        return team_names

    def is_complete(self):
        return False


class PendingGameAnalyser(GameAnalyser):
    STATE = PENDING

    def process(self):
        my_condition = self.find_condition()
        team_names = self.get_team_names()

        class_name = my_condition["wait_class_name"]
        target_nodes = self.soup.select(f".{class_name}")
        
        matchup_prediction = target_nodes[0].text
        matchup_prediction = matchup_prediction.replace("%", " ").split(" ")

        # Time is in the div with this class name
        time_div_classname = "Gamestrip__Time--wrapper"
        game_time_div = self.soup.select(f".{time_div_classname}")[0]
        game_time = game_time_div.text    

        matchup_payload = self.create_payload(
            MLB_TEAM_NAMES_MAP[team_names[0]],
            MLB_TEAM_NAMES_MAP[team_names[1]],
            matchup_prediction[0],
            matchup_prediction[1]
        )
        return matchup_payload

    def is_complete(self):
        return False


class CompletedGameAnalyser(GameAnalyser):
    STATE = COMPLETED

    def process(self):
        my_condition = self.find_condition()
        team_names = self.get_team_names()

        class_name = my_condition["wait_class_name"]
        target_nodes = self.soup.select(f".{class_name}")
        
        matchup_prediction = target_nodes[0].text
        matchup_prediction = matchup_prediction.replace("%", " ").split(" ")
        for_team = self.soup.select(f".{class_name} img")[0]
        
        matchup_payload = CompletedGameAnalyser.create_payload(
            MLB_TEAM_NAMES_MAP[team_names[0]],
            MLB_TEAM_NAMES_MAP[team_names[1]],
            matchup_prediction[0],
            matchup_prediction[1]
        )
        return matchup_payload

    def is_complete(self):
        return True


analyser_factory = {
    LIVE: LiveGameAnalyser,
    PENDING: PendingGameAnalyser,
    COMPLETED: CompletedGameAnalyser,
}


if __name__ == "__main__":
    page_source, args = load_page_source()
    condition_mapping = load_conditions(CONDITIONS_FILENAME)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    page_state = identify_page_state(condition_mapping, soup)

    analyser = analyser_factory[page_state](soup, args, condition_mapping)
    print(analyser.process())
    