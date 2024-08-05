from bs4 import BeautifulSoup
from webpage_loader import load_page_source


if __name__ == "__main__":
    page_source, args = load_page_source()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    class_names = ".".join(args.wait_class_names.split())
    target_nodes = soup.select(f".{args.wait_class_names}")

    # Get teams competing from url
    team_names = args.url.split("/")[-1].split("-")
    matchup_prediction = target_nodes[0].text
    matchup_prediction = matchup_prediction.replace("%", " ").split(" ")

    print("Matchup Below")
    print(f"{team_names[0]}: {matchup_prediction[0]}")
    print(f"{team_names[1]}: {matchup_prediction[1]}")