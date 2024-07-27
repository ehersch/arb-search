import requests
import json


# We use this function to enter a bet on a certain matchup to our Mongo.
# We enter the data by matchup (i.e. "Baltiore OriolesNew York Yankees")
# of the format t1 + t2 where t1 comes firts alphabetically. Then we hold
# odds_a and odds_b, where odds_a is the odds we placed a bet for team1 and
# odds_b the same for team 2. Then amt_a and amt_b are the  bet amounts.
def main(site, t1, t2, time, odds_a, odds_b, amt_a, amt_b):
    # findOne to get, insertOne to add
    url = "https://us-east-2.aws.data.mongodb-api.com/app/data-jhkosvr/endpoint/data/v1/action/insertOne"

    data = {
        "site": site,
        "matchup": t1 + t2,
        "time": time,
        "odds_a": odds_a,
        "odds_b": odds_b,
        "amt_a": amt_a,
        "amt_b": amt_b,
    }

    addition = json.dumps(
        {
            "collection": "previous-bets",
            "database": "arb-search",
            "dataSource": "Crud",
            "document": data,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": "***",
    }

    response = requests.request("POST", url, headers=headers, data=addition)

    print(response.text)


if __name__ == "__main__":
    main()
