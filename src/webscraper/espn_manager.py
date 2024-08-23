import ast
import subprocess as sp


GET_URLS_SCRIPT_RELATIVE_PATH = "./scrape_urls.py"
GET_PREDICTIONS_SCRIPT_RELATIVE_PATH = "./scrape_predictions.py"


def get_urls_for_today():
    urls = sp.getoutput(
        f"python3 {GET_URLS_SCRIPT_RELATIVE_PATH} --headless --url https://www.espn.com/mlb/schedule"
    )
    return urls


if __name__ == "__main__":
    urls = get_urls_for_today()
    urls = urls.split()
    urls_string = ",".join(urls)

    output = sp.getoutput(
        " ".join([
            "python3",
            GET_PREDICTIONS_SCRIPT_RELATIVE_PATH,
            "--headless",
            "--urls",
            urls_string
        ])
    )
    payloads = [ast.literal_eval(o) for o in output.split("\n")]
    print(output)