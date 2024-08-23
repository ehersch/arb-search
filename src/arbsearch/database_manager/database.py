import use_db
from abc import ABC, abstractmethod
import sqlite3
import csv

from pydantic import BaseModel

PATH_TO_CREATION_LOGIC = "./sql_table_creation.txt"


class MatchupSchema(BaseModel):
    away_team: str
    home_team: str
    home_team_matchup_probability: float
    away_team_odds: float
    home_team_odds: float


class DatabaseInterface(ABC):
    def __init__(self, path):
        self.path = path
        print("Database initialized")

    @abstractmethod
    def insert_data(self, data: MatchupSchema):
        pass


class SQLDatabase(DatabaseInterface):

    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        # Drop the table if it already exists
        # cur.execute('DROP TABLE IF EXISTS game_forecasts')

        # Create the game_forecasts table
        with open(PATH_TO_CREATION_LOGIC, "r") as sql_create:
            sql_command = sql_create.readlines()
            cur.execute(sql_command)

        # Commit the changes and close the connection
        con.commit()
        con.close()
