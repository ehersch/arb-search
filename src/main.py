from pathlib import Path

from arbsearch import SQLDatabase, DatabaseInterface
from odds_collector import OddsAPICollection, OddsCollectionInterface

# Get the directory of the current file
current_dir = Path(__file__).parent
DATABASE_DIR = current_dir / "databases"

# Should be programmatically extracted
site_keys = [
    "fanduel",
    "draftkings",
    "mybookieag",
    "betmgm",
    "bovada",
    "williamhill_us",
    "wynnbet",
]

class CollectionManager:
    def __init__(
            self,
            dbs: list[DatabaseInterface],
            odds_collector: OddsCollectionInterface 
        ):
        self.dbs = dbs

    
    def collect_data(self):
        pass
            


def main():
    booky_db_paths = [f"{DATABASE_DIR}/{booky}.db" for booky in site_keys]
    booky_dbs = [SQLDatabase(booky_path) for booky_path in booky_db_paths]
    odds_collector = OddsAPICollection()

    cm = CollectionManager(booky_dbs, odds_collector)

    # dbs = {booky: SQLDatabase(booky) for booky in booky_names}

if __name__ == "__main__":
    main()