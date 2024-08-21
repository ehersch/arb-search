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

    if condition == "final":
        return COMPLETED
    elif condition == "live":
        return LIVE
    else:
        return PENDING
    

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
    
    def get_team_names(self):
        team_names_class = "ScoreCell__TeamName"
        team_names = self.soup.select(f".{team_names_class}")
        team_names = [team_names[0].text.lower(), team_names[1].text.lower()]
        return team_names

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
        pass

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

        class_name = my_condition["wait_class_name"]
        target_nodes = self.soup.select(f".{class_name}")

        # Get teams competing from url
        team_names_class = "ScoreCell__TeamName"
        team_names = self.soup.select(f".{team_names_class}")
        team_names = [team_names[0].text.lower(), team_names[1].text.lower()]
        
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
    