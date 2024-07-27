# Here find current arb opportunities (irrespective of previous bets).
# Here enter previous bets made on a certain matchup (MongoDB).
# Here look at current arb based on previous bets made.
import sys
from logic import find_arb, enter_bets, get_bets
from cols import parse_json

# TODO write a function to parse time from the odds API and interpet it for the user.


def main():
    parse_json.main("data/test.json")
    print("Welcome to ArbSearch.")
    action = input("Search for current arbitrage? (y/n)\n")

    if action == "y":
        res = find_arb.main()
        if res == None:
            print("There are no opportunities")
        else:
            print(
                f"There is arbitrage available.\n{res['site_a']}: {res['t1']} for {res['val_a']}\n{res['site_b']}: {res['t2']} for {res['val_b']} playing at {res['time']}."
            )
            amt = input("Enter your desired bet quantity.\n")
            (team_a, x, a), (team_b, y, b) = split(int(amt), res)

            enter = input("Press 'return' to enter this bet.\n")
            if enter == "":
                enter_bets.main(team_a, team_b, a, b, x, y)
    else:

        action = input("Find arbitrage based off past bets? (y/n)\n")
        # TODO: We should change this code so that it does the following: retrieve
        # all past bets on games whose odds are currently listed. See if for some
        # bet we placed in the past we can bet on the opponent now and find
        # ourselves in arbitrage.
        if action == "y":
            # Retrieve current matchups and their odds
            data = parse_json.main("data/test.json")
            current_matchups = {key: value for key, value in data.items()}

            arbitrage_opportunities = []

            # Check if any past bets can now create arbitrage opportunities
            for key in current_matchups:
                team1, team2, time = key
                current_odds = current_matchups[key]

                # Retrieve past bets for the current matchup
                past_bets = get_bets.main(team1, team2, time)

                if past_bets:
                    past_odds_a, amt_a, past_odds_b, amt_b = past_bets
                    for site, odds in current_odds:
                        current_odds_a, current_odds_b = odds
                        # Compare current odds with past odds to find arbitrage
                        arb_opportunity = check_arbitrage(
                            team_1,
                            team_2,
                            past_odds_a,
                            amt_a,
                            past_odds_b,
                            amt_b,
                            current_odds_a,
                            current_odds_b,
                        )
                        if arb_opportunity:
                            arbitrage_opportunities.append(arb_opportunity)

            if arbitrage_opportunities:
                for opportunity in arbitrage_opportunities:
                    print(f"Arbitrage Opportunity:\n{opportunity}")
            else:
                print("No arbitrage opportunities based on past bets.")


def check_arbitrage(past_bet, current_odds, site_a, site_b, time, t1, t2):
    """
    Check if there is an arbitrage opportunity based on past and current odds.

    Args:
        past_odds_a (float): The average odds for team 1 from past bets.
        current_odds_a (float): The current odds for team 1.
        past_odds_b (float): The average odds for team 2 from past bets.
        current_odds_b (float): The current odds for team 2.

    Returns:
        dict or None: Returns a dictionary with arbitrage opportunity details if found,
                      otherwise returns None.
    """
    team_a, team_b, past_odds_a, amt_a, past_odds_b, amt_b = past_bet

    # Calculate implied probabilities for past odds
    if past_odds_a > 0:
        odd_a = 100 / (past_odds_a + 100)
    else:
        odd_a = (-past_odds_a) / ((-past_odds_a) + 100)

    if past_odds_b > 0:
        odd_b = 100 / (past_odds_b + 100)
    else:
        odd_b = (-past_odds_b) / ((-past_odds_b) + 100)

    # Calculate implied probabilities for current odds
    if current_odds[0] > 0:
        current_odd_a = 100 / (current_odds[0] + 100)
    else:
        current_odd_a = (-current_odds[0]) / ((-current_odds[0]) + 100)

    if current_odds[1] > 0:
        current_odd_b = 100 / (current_odds[1] + 100)
    else:
        current_odd_b = (-current_odds[1]) / ((-current_odds[1]) + 100)

    # Check for arbitrage opportunity
    if (odd_a + current_odd_b < 1) or (current_odd_a + odd_b < 1):
        arbitrage_opportunity = {
            "site_a": site_a,
            "site_b": site_b,
            "time": time,
            "t1": t1,
            "t2": t2,
            "a": current_odds[0],
            "b": current_odds[1],
            "val_a": ___,
            "val_b": ___,
            # TODO figure out amounts for each
        }
        return arbitrage_opportunity

    return None


# Calculate the split for betting.
# I.e. how much must we bet on either team to maximize arb?
def split(amt, res):
    tot = res["a"] + res["b"]

    # assume a > 0
    # solve equation: amount of money made from team a winning equals
    # amount of money made from team b winning.
    # find x st (x * a/100 - (amt - x) = (amt - x) * (100/-b) - (x))
    # ax/100 + 100(amt-x)/b + 2x == amt
    # x(a/100 + 2) - 100 * x/b = amt - 100 * amt/b
    # x  = (amt -100 * amt/b) / (a/100 + 2 - 100/b)

    a = max(int(res["val_a"]), int(res["val_b"]))
    team_a = team_b = ""

    if int(res["val_a"]) > int(res["val_b"]):
        a = int(res["val_a"])
        team_a = res["t1"]
        b = int(res["val_b"])
        team_b = res["t2"]

    else:
        a = int(res["val_b"])
        team_a = res["t2"]
        b = int(res["val_a"])
        team_b = res["t1"]

    b = min(int(res["val_a"]), int(res["val_b"]))
    denom = a / 100 + 2 - (100 / b)
    num = amt - 100 * (amt / b)
    x = num / denom
    profit = x * a / 100 - amt + x
    print(f"Bet {x} on {team_a} and {amt-x} on {team_b} to profit {profit}")
    return (team_a, x, a), (team_b, amt - x, b)


if __name__ == "__main__":
    main()
