"""
Script to identify baseball arbitrage opportunities based on odds data.

This script parses data containing baseball odds from various betting sites
and checks for arbitrage opportunities. An arbitrage opportunity exists if
the sum of the inverse odds for the two teams in a match is less than 1,
indicating a guaranteed profit regardless of the outcome.

Functions:
    main(): Main function that iterates through matchups and identifies arbitrage opportunities.
    individual_arb(data): Analyzes the odds for a single matchup to find the best odds for each team.

Modules:
    sys, os: Used for adjusting the system path.
    parse_json: Custom module to parse odds data from JSON.

Example usage:
    Run this script to print any identified arbitrage opportunities.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from odds_collector import parse_json

data = parse_json.main()


def main():
    """
    Main function to parse baseball odds data and find arbitrage opportunities.

    This function retrieves the odds data, iterates over each matchup, and
    passes the data to the individual_arb function to check for arbitrage
    opportunities. If an opportunity is found, it is printed and returned.

    Returns:
        dict: A dictionary containing details of the arbitrage opportunity
              if found, otherwise None.
    """
    data = parse_json.main()
    print(len(data))
    for (away, home, time), lst in data.items():
        ((a, site_a), (b, site_b), (val_a, val_b)) = individual_arb({(away, home): lst})
        if a + b < 1:

            f = {
                "site_a": site_a,
                "site_b": site_b,
                "time": time,
                "t1": away,
                "t2": home,
                "a": a,
                "b": b,
                "val_a": val_a,
                "val_b": val_b,
            }

            # print(site_a + ": " + str(a) + " on " + t1)
            # print(site_b + ": " + str(b) + " on " + t2)
            return f
    return None


def individual_arb(data):
    """
    Determine the best odds for each team in a given matchup to find arbitrage opportunities.

    Args:
        data (dict): A dictionary containing matchup data with team names as keys
                     and a list of (site, odds) tuples as values.

    Returns:
        tuple: A tuple containing:
               - ((float, str), (float, str)): Best odds and corresponding site for team 1 and team 2.
               - (float, float): Original odds for team 1 and team 2.
    """
    min_a = min_b = 1
    [lst] = data.values()
    site_a = site_b = ""

    for site, [a, b] in lst:
        if a > 0:
            odd_a = 100 / (a + 100)
        if a < 0:
            odd_a = (-a) / ((-a) + 100)
        temp = min_a

        # TODO: ensure not pulling from same 2 sites. We should verify this.
        if odd_a < min_a and site != site_b:
            min_a = odd_a
            val_a = a
            site_a = site

        if temp != min_a:
            site_a = site

        if b > 0:
            odd_b = 100 / (b + 100)
        if b < 0:
            odd_b = (-b) / ((-b) + 100)
        temp = min_b

        # TODO: ensure not pulling from same 2 sites. We should verify this.
        if odd_b < min_b and site != site_a:
            min_b = odd_b
            val_b = b
            site_b = site

        if temp != min_b:
            site_b = site

    return ((min_a, site_a), (min_b, site_b), (val_a, val_b))


if __name__ == "__main__":
    main()
