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
import arbsearch.odds_collector.read_api as read_api
# import arbsearch.cols.parse_json
# from sql import use_db
# from webscraper import scrape_manager
# from datetime import datetime

def collect_day():
    return 21
# def collect_day():
#     """
#     Continuously fetches, parses, and stores baseball odds data in a database for one day. Run once every day.

#     This function runs an infinite loop that performs the following tasks every hour:
#     1. Writes data to a JSON file using read_api.write_to.
#     2. Parses the JSON file to extract odds information.
#     3. Inserts the parsed data into a SQLite database.

#     Note:
#         - The `win_percentage1` and `win_percentage2` variables are placeholders and need to be
#           implemented to fetch actual win percentages.
#         - The script will run indefinitely until manually stopped.

#     Example:
#         This function is executed when the script is run directly.
#     """
#     i = 1
#     while True:
#         now = datetime.now()

#         # End if it's 1:00 AM
#         if now.hour == 1:
#             return
#         # Fetch and write odds data to a JSON file
#         read_api.write_to(f"odds{i}.json")

#         # Parse the JSON file to extract odds data
#         data = parse_json.main(f"odds{i}.json")

#         # Iterate through the parsed data and insert it into the database
#         for (t1, t2, time), lst in data.items():
#             [lst] = data.values()
#             for site, [a, b] in lst:
#                 # Placeholder for actual win percentages
#                 win_percentage = probability_dict[(t1, t2)]
#                 # TODO: Get actual win percentage for team 1

#                 # teams are ordered by (home, away)
#                 use_db.insert(
#                     "data/baseball_forecasting.db", t1, t2, win_percentage, a, b
#                 )

#         i += 1

#         # Wait for 10 minutes before checking again during game time
#         # (between 1:00 pm and 5:30 pm or 6:30 pm to end).
#         # Otherwise, wait 30 minutes
#         now = datetime.now()

#         if (now.hour > 10 and now.hour < 13) or (
#             (now.hour > 5 and now.minute > 30) and (now.hour < 5 and now.minute < 30)
#         ):
#             time.sleep(1800)

#         else:
#             time.sleep(600)


# def main():
#     """
#     Start running at 9 am first day. Every 10 minutes from 9 am to 11 pm game data will be collected.
#     """

#     def wait_until_10_am():
#         while True:
#             # Get the current time
#             now = datetime.now()

#             # Check if it's 10:00 AM
#             if now.hour == 10 and now.minute == 0:
#                 collect_day()
#                 break  # Exit the loop and stop the script after doing something

#             time.sleep(30)


# if __name__ == "__main__":
#     main()
