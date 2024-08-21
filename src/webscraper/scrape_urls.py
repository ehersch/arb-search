import datetime
from bs4 import BeautifulSoup
from webpage_loader import load_page_source


if __name__ == "__main__":
    """The classname we primarily care about on the ESPN website is "ScheduleTables". This class is attached
    to every table that is loaded on the website. Invoking this script is done as follows:

    python3 get_mlb_game_urls.py --driver_path <path_to_driver> --url https://www.espn.com/mlb/schedule --headless \
    --wait_class_names "ScheduleTables"

    When this is executed, this script should print to the terminal all the links of games that are currently live
    or yet to be played.
    """
    page_source, args = load_page_source()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    class_names = ".".join(args.wait_class_names.split())
    target_nodes = soup.select(f".{args.wait_class_names}")

    """TODO:
    Everything below this line should be in a file for scrapping scheduled games from the schedule page. Then we can
    have a separate script for getting the game IDs so we can collect the matchup prediction in another script. The logic
    above stays the same in both cases. Hence, we'll do something along the lines of:
      - python3 get_urls.py | python3 get_matchup_predictions.py 

    Matchup predictions are updated live during a game, so we need to write some logic for handling this. Idealy, we can
    get the time the game starts and write some type of chron task for handling this.
    """
    # The element in the table that we care about has the following class names: date__col Table__TD
    time_class_names = ["date__col", "Table__TD"]

    # Maintain a set for all the links of interest
    hyperlinks = set()

    # Grab all the links for each game presented in the tables
    for target_node in target_nodes[1:2]:
        # Each descendant in the current target node is a row in the schedule
        for descendant in target_node.descendants:
            tcn = "." + ".".join(time_class_names)
            # The try-except clause is to ignore grabbed elements where the game
            # is already finished
            try:
                # Extract the link from the "a" tag associated with the date column
                td_element = descendant.select(tcn)[0]
                a_element = td_element.find("a", class_="AnchorLink")
                hyperlinks.add(a_element.get("href"))
            except:
                pass

    # Assumes we are using .com websites only. Should be refactored
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f"{current_date}_game_urls.txt"
    with open(f"./data/urls/{filename}", "w") as todays_urls_file:
        com_index = args.url.find(".com") + 4 # len(".com") = 4
        base_url = args.url[:com_index]
        for hl in hyperlinks:
            todays_urls_file.write(f"{base_url}{hl}\n")