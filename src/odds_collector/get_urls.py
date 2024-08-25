import requests
from bs4 import BeautifulSoup

# Define the URL
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def main():

    res = []

    # Configure Selenium to use the Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_service = Service(
        "/Users/ethanhersch/Downloads/chromedriver-mac-arm64/chromedriver"
    )  # Update this with the path to your chromedriver

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Define the URL
    url = "https://www.espn.com/mlb/schedule"

    # Open the webpage
    driver.get(url)
    # # Wait for the necessary elements to load
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Table__TBODY"))
    )
    # time.sleep(1)
    # Get the page source
    page_source = driver.page_source
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    data = soup.find("tbody", class_="Table__TBODY")
    data = data.find_all("td", class_="date__col Table__TD")
    for d in data:
        res.append((d.find("a").get("href")))
    # for a in data:
    #     print(a.get("href"))
    # Close the browser
    driver.quit()

    base = "https://www.espn.com"

    ans = []

    for link in res:
        ans.append(base + link)

    return ans


if __name__ == "__main__":
    print(main())
