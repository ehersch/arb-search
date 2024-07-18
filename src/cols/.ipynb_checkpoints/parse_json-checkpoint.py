import json
from collections import defaultdict


# Parse this JSON into a more manageable format.
# The format is a dictionary where the key is the matchup
# (e.i "Baltimore Orioles vs. New York Yankees"), which is always alphabetical
# and the vale is a list of the sites and their odds (as a tuple).
# The first odd in the list corresponds with the first alphabetical team.
# The key must also include the game time: in the event of a double header,
# odds can be posted for two games with the same matchup. It is safest to also
# keep track of game time
# example {"(Baltimore Orioles, New York Yankees, 1720564560)" : [("Draft Kings", [-110, +110]), ("MGM", [-120, +120])]}
def main(filename):
    # this line changes based on which json file we want to 'clean up'
    # for testing purposes, we clean up odds1.json
    f = open(filename)
    data = json.load(f)

    g = open("data/teams.json")
    teams = json.load(g)

    num_games = len(data["data"])
    matchups = defaultdict(list)

    for i in range(num_games):
        team1 = data["data"][i]["teams"][0]
        team2 = data["data"][i]["teams"][1]
        time = data["data"][i]["commence_time"]
        key = (team1, team2, time)
        lst = []
        num_sites = data["data"][i]["sites_count"]
        for j in range(num_sites):
            site = data["data"][i]["sites"][j]["site_key"]
            odds = data["data"][i]["sites"][j]["odds"]["h2h"]
            lst.append((site, odds))
        matchups[key] = lst
    return matchups


if __name__ == "__main__":
    main()
