import requests
import json


# We use this function to find past bet on a certain matchup from our Mongo.
# We look up the bets by matchup filtering by matchup
# (i.e. "Baltiore OriolesNew York Yankees") of the format t1 + t2 where t1 comes
# firts alphabetically. We  also filter based on time because odds can be posted
# for games with the same matchup. Then we hold  odds_a and odds_b, where odds_a
# is the odds we placed a bet for team1 and odds_b the same for team 2. Then
#  amt_a and amt_b are the  bet amounts.
def main(away, home, time):
    # findOne to get, insertOne to add
    url = "https://us-east-2.aws.data.mongodb-api.com/app/data-jhkosvr/endpoint/data/v1/action/findOne"

    filt = json.dumps(
        {
            "collection": "previous-bets",
            "database": "arb-search",
            "dataSource": "Crud",
            "filter": {"matchup": away + home, "time": time},
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": "***",
    }

    a_sites = set()
    b_sites = set()

    response = requests.request("POST", url, headers=headers, data=filt)
    data = response.json()
    print(data["document"]["odds_a"])
    away_odds = 0.0
    home_odds = 0.0
    away_total = 0.0
    home_total = 0.0
    for instance in data.get("document", []):
        odds_a = float(instance["data"]["odds_a"])
        odds_b = float(instance["data"]["odds_b"])
        amt_a = float(instance["data"]["amt_a"])
        amt_b = float(instance["data"]["amt_b"])
        if amt_b == 0:
            a_sites.append(instance["data"]["site"])
        if amt_a == 0:
            b_sites.append(instance["data"]["site"])
        away_odds += odds_a * amt_a
        home_odds += odds_b * amt_b
        away_total += amt_a
        home_total += amt_b

    return (
        a_sites,
        b_sites,
        away,
        home,
        float(away_odds / float(away_total)),
        away_total,
        float(home_odds / float(home_total)),
        home_total,
    )


if __name__ == "__main__":
    main()
