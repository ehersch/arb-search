import sqlite3

from abc import ABC, abstractmethod
from pathlib import Path
from pydantic import BaseModel


# Get the directory of the current file
current_dir = Path(__file__).parent

# Construct the absolute paths
PATH_TO_CREATION_LOGIC = current_dir / "sql_table_creation.txt"
PATH_TO_INSERTION_LOGIC = current_dir / "sql_table_insertion.txt"
MATCHUP_PREDICTIONS_DATABASE = current_dir / "matchup_predictions.db"


class MatchupSchema(BaseModel):
    away_team: str
    home_team: str
    home_team_win_probability: float
    away_team_odds: float
    home_team_odds: float


class DatabaseInterface(ABC):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def insert_data(self, data: MatchupSchema):
        pass


class SQLDatabase(DatabaseInterface):
    def __init__(self, path):
        super().__init__(path)
        self.create()

    def create(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        # Create the game_forecasts table
        with open(PATH_TO_CREATION_LOGIC, "r") as sql_create:
            sql_command = sql_create.read()
            cur.execute(sql_command)

        # Commit the changes and close the connection
        con.commit()
        con.close()

    def insert_data(self, data: MatchupSchema):
        # Connect to the database
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        # SQL insert statement
        with open(PATH_TO_INSERTION_LOGIC, "r") as sql_insert:
            sql_command = sql_insert.read()
            # Execute the insert statement with data from MatchupSchema
            cur.execute(sql_command, (
                data.away_team,
                data.home_team,
                data.home_team_win_probability,
                data.away_team_odds,
                data.home_team_odds
            ))

        # Commit the changes and close the connection
        con.commit()
        con.close()


if __name__ == "__main__":
    # Toy data
    toy_data = [
        MatchupSchema(
            away_team="Yankees",
            home_team="Red Sox",
            home_team_win_probability=0.55,
            away_team_odds=2.5,
            home_team_odds=1.8
        ),
        MatchupSchema(
            away_team="Dodgers",
            home_team="Giants",
            home_team_win_probability=0.65,
            away_team_odds=2.1,
            home_team_odds=1.7
        ),
        MatchupSchema(
            away_team="Mets",
            home_team="Phillies",
            home_team_win_probability=0.60,
            away_team_odds=2.2,
            home_team_odds=1.9
        )
    ]

    # Initialize the database
    db = SQLDatabase(MATCHUP_PREDICTIONS_DATABASE)

    # Insert toy data into the database
    for matchup in toy_data:
        db.insert_data(matchup)

    print("Data has been inserted successfully.")