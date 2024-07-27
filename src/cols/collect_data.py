"""
Script to periodically fetch baseball odds data, parse it, and store it in a database.

This script runs in an infinite loop, fetching odds data from an API every hour,
parsing the data, and then inserting it into a SQLite database. It handles data
for baseball forecasting by writing it into a file, parsing the file to extract
odds information, and then storing this information in the database.

Functions:
    main(): Main function that performs the periodic data fetch, parse, and database insert operations.

Modules:
    time: Used for pausing execution between data fetches.
    src.cols.read_api: Custom module to fetch and write odds data to a file.
    parse_json: Custom module to parse JSON data from the file.
    sql: Custom module for database operations.

Example usage:
    Run this script to continuously fetch, parse, and store baseball odds data every hour.
"""

import time
import src.cols.read_api as read_api
import parse_json
from sql import use_db


def main():
    """
    Continuously fetches, parses, and stores baseball odds data in a database.

    This function runs an infinite loop that performs the following tasks every hour:
    1. Writes data to a JSON file using read_api.write_to.
    2. Parses the JSON file to extract odds information.
    3. Inserts the parsed data into a SQLite database.

    Note:
        - The `win_percentage1` and `win_percentage2` variables are placeholders and need to be
          implemented to fetch actual win percentages.
        - The script will run indefinitely until manually stopped.

    Example:
        This function is executed when the script is run directly.
    """
    i = 1
    while True:
        # Fetch and write odds data to a JSON file
        read_api.write_to(f"odds{i}.json")

        # Parse the JSON file to extract odds data
        data = parse_json.main(f"odds{i}.json")

        # Iterate through the parsed data and insert it into the database
        for (t1, t2, time), lst in data.items():
            [lst] = data.values()
            for site, [a, b] in lst:
                # Placeholder for actual win percentages
                win_percentage1 = 0  # TODO: Get actual win percentage for team 1
                win_percentage2 = 0  # TODO: Get actual win percentage for team 2

                use_db.insert(
                    "data/baseball_forecasting.db", t1, t2, win_percentage1, a, b
                )
                use_db.insert(
                    "data/baseball_forecasting.db", t2, t1, win_percentage2, b
                )

        i += 1
        time.sleep(3600)  # Sleep for 1 hour (3600 seconds)


if __name__ == "__main__":
    main()
