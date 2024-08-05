import sqlite3
import csv


def create(path):
    con = sqlite3.connect(path)
    cur = con.cursor()
    # Drop the table if it already exists
    # cur.execute('DROP TABLE IF EXISTS game_forecasts')

    # Create the game_forecasts table
    cur.execute(
        """
      CREATE TABLE IF NOT EXISTS game_forecasts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          team_a TEXT NOT NULL,
          team_b TEXT NOT NULL,
          win_percentage REAL NOT NULL,
          team_a_odds REAL NOT NULL,
          team_b_odds REAL NOT NULL
      )
  """
    )

    # Commit the changes and close the connection
    con.commit()
    con.close()


def insert(path, team_a, team_b, win_percentage, team_a_odds, team_b_odds):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO game_forecasts (team_a, team_b, win_percentage, team_a_odds, team_b_odds)
        VALUES (?, ?, ?, ?, ?)
    """,
        (team_a, team_a, win_percentage, team_a_odds, team_b_odds),
    )

    conn.commit()
    conn.close()


# Example usage
# insert("Team A", "Team B", 0.65, 1.5)


def get(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM game_forecasts")
    rows = cursor.fetchall()
    print(len(rows))

    for row in rows:
        print(row)

    conn.close()


def export_to_csv(database_path, csv_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Select all data from the game_forecasts table
    cursor.execute("SELECT * FROM game_forecasts")
    rows = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [description[0] for description in cursor.description]

    # Open the CSV file for writing
    with open(csv_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the column names as the first row
        csv_writer.writerow(column_names)

        # Write the data rows
        csv_writer.writerows(rows)

    # Close the database connection
    conn.close()


# Example usage
def print_csv(csv_path):
    # Open the CSV file for reading
    with open(csv_path, newline="") as csv_file:
        csv_reader = csv.reader(csv_file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            print(row)


# Example usage
db_path = "data/baseball_forecasting.db"
csv_path = "data/game_forecasts.csv"
# create(db_path)
# insert(db_path, "Team A", "Team B", 0.65, 1.5, 1.2)
# export_to_csv(db_path, csv_path)
# get(db_path)
