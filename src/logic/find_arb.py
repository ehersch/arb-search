import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cols import parse_json

data = parse_json.main()


# Given the odds generated from API call, find if there are any current baseball
# arbitrage opportunities.
# Parse through every matchup and pass each into individual_arb.
def main():
    data = parse_json.main()
    print(len(data))
    for (t1, t2, time), lst in data.items():
        ((a, site_a), (b, site_b), (val_a, val_b)) = individual_arb({(t1, t2): lst})
        if a + b < 1:

            f = {
                "site_a": site_a,
                "site_b": site_b,
                "time": time,
                "t1": t1,
                "t2": t2,
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
