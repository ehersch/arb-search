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
        if action == "y":
            team_1 = input("Input team 1 (caps with city -- ex: Los Angeles Angels).\n")
            team_2 = input("Input team 2 (caps with city -- ex: Los Angeles Angels).\n")
            lst = [team_1, team_2]
            lst.sort()
            [a, b] = lst
            print(get_bets.main(a, b))


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
