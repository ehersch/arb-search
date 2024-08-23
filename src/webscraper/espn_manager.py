import ast
import subprocess as sp


GET_URLS_SCRIPT_RELATIVE_PATH = "./scrape_urls.py"
GET_PREDICTIONS_SCRIPT_RELATIVE_PATH = "./scrape_predictions.py"


class ESPNManager:
    def __init__(self):
        self.urls = self._get_urls_for_today()

    def _get_urls_for_today(self):
        urls = sp.getoutput(
            f"python3 {GET_URLS_SCRIPT_RELATIVE_PATH} --headless --url https://www.espn.com/mlb/schedule"
        )
        urls = urls.split()
        
        return urls
    
    def get_payload(self):
        urls_string = ",".join(self.urls)
        output = sp.getoutput(f"python3 {GET_PREDICTIONS_SCRIPT_RELATIVE_PATH} --headless --urls {urls_string}")
        payloads = [ast.literal_eval(o) for o in output.split("\n")]
        return payloads


if __name__ == "__main__":
    print(ESPNManager().get_payload())