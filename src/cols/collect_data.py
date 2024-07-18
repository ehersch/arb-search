import time
import api
import parse_json
from sql import use_db


def main():
    i = 1
    while True:
        api.main(f"odds{i}.json")
        data = parse_json.main(f"odds{i}.json")
        for (t1, t2, time), lst in data.items():
            [lst] = data.values()
            for site, [a, b] in lst:
                use_db.insert(
                    "data/baseball_forecasting.db", t1, t2, win_percentage1, a
                )
                use_db.insert(
                    "data/baseball_forecasting.db", t2, t1, win_percentage2, b
                )
          TODO get win percentages
        i += 1
        time.sleep(3600)  # Sleep for 1 hour (3600 seconds)


# Example usage
if __name__ == "__main__":
    main()
