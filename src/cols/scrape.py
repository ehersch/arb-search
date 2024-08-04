import argparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverManager:
    """
    A class to manage different web drivers (Chrome, Firefox, Edge, Safari) for web scraping or automated browsing tasks.

    Attributes:
        driver_path (str): Path to the web driver executable.
        driver_type (str): Type of the web driver (default is "chrome").
        headless (bool): Whether to run the browser in headless mode (default is False).
        driver: The web driver instance.

    Methods:
        _initialize_driver(): Initializes and returns the web driver based on the specified type and options.
        open_page(url: str, wait_for_class_names: str = None, timeout: int = 10): Opens the specified URL and waits for the specified element class names if provided.
        close(): Closes the web driver.
    """

    def __init__(
        self, driver_path: str, driver_type: str = "chrome", headless: bool = False
    ):
        """
        Initializes the WebDriverManager with the specified driver path, driver type, and headless option.

        Args:
            driver_path (str): Path to the web driver executable.
            driver_type (str): Type of the web driver (default is "chrome").
            headless (bool): Whether to run the browser in headless mode (default is False).
        """
        self.driver_path = driver_path
        self.driver_type = driver_type.lower()
        self.headless = headless
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """
        Initializes and returns the web driver based on the specified type and options.

        Returns:
            WebDriver: The initialized web driver instance.

        Raises:
            ValueError: If the specified driver type is unsupported.
        """
        if self.driver_type == "chrome":
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            service = ChromeService(executable_path=self.driver_path)
            return webdriver.Chrome(service=service, options=options)
        elif self.driver_type == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            service = FirefoxService(executable_path=self.driver_path)
            return webdriver.Firefox(service=service, options=options)
        elif self.driver_type == "edge":
            options = EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            service = EdgeService(executable_path=self.driver_path)
            return webdriver.Edge(service=service, options=options)
        elif self.driver_type == "safari":
            options = SafariOptions()
            if self.headless:
                options.add_argument("--headless")
            service = SafariService(executable_path=self.driver_path)
            return webdriver.Safari(service=service, options=options)
        else:
            raise ValueError("Unsupported driver type: {}".format(self.driver_type))

    def open_page(self, url: str, wait_for_class_names: str = None, timeout: int = 11):
        """
        Opens the specified URL and waits for the specified element class names if provided.

        Args:
            url (str): The URL of the page to open.
            wait_for_class_names (str, optional): Space-separated class names of the element to wait for (default is None).
            timeout (int, optional): The maximum time to wait for the element in seconds (default is 10).

        Returns:
            str: The page source of the opened URL.
        """
        self.driver.get(url)

        if wait_for_class_names:
            wait_for_class_names = ".".join(wait_for_class_names.split())

            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f".{wait_for_class_names}")
                )
            )

        return self.driver.page_source

    def close(self):
        """
        Closes the web driver.
        """
        self.driver.quit()


def main():
    """The classname we primarily care about on the ESPN website is "ScheduleTables". This class is attached
    to every table that is loaded on the website. Invoking this script is done as follows:

    python3 scrape.py --driver_path <path_to_driver> --url https://www.espn.com/mlb/schedule --headless \
    --wait_class_name "ScheduleTables"

    When this is executed, this script should print to the terminal all the links of games that are currently live
    or yet to be played.
    """
    parser = argparse.ArgumentParser(
        description="A command line tool to open a web page using Selenium and BeautifulSoup."
    )
    parser.add_argument(
        "--driver_path", type=str, help="Path to the WebDriver executable."
    )
    parser.add_argument("--url", type=str, help="URL of the web page to open.")
    parser.add_argument(
        "--driver_type",
        type=str,
        default="chrome",
        help="Type of WebDriver to use (chrome, firefox, edge, safari).",
    )
    parser.add_argument(
        "--headless", action="store_true", help="Run browser in headless mode."
    )
    parser.add_argument(
        "--wait_class_names",
        type=str,
        default=None,
        help="Class name of the element to wait for.",
    )

    args = parser.parse_args()

    # Ensures the webpage is loaded by waiting for user specified class names to load
    manager = WebDriverManager(args.driver_path, args.driver_type, args.headless)
    page_source = manager.open_page(
        args.url, wait_for_class_names=args.wait_class_names
    )

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    class_names = ".".join(args.wait_class_names.split())
    target_nodes = soup.select(f".{args.wait_class_names}")

    # The element in the table that we care about has the following class names: date__col Table__TD
    time_class_names = ["date__col", "Table__TD"]

    # Maintain a set for all the links of interest
    hyperlinks = set()

    # Grab all the links for each game presented in the tables
    for target_node in target_nodes[1:2]:
        # Each descendant in the current target node is a row in the schedule
        for descendant in target_node.descendants:
            tcn = "." + ".".join(time_class_names)
            # The try-except clause is to ignore grabbed elements where the game
            # is already finished
            try:
                # Extract the link from the "a" tag associated with the date column
                td_element = descendant.select(tcn)[0]
                a_element = td_element.find("a", class_="AnchorLink")
                hyperlinks.add(a_element.get("href"))
            except:
                pass

    # Assumes we are using .com websites only. Should be refactored
    com_index = args.url.find(".com") + 4  # len(".com") = 4
    base_url = args.url[:com_index]
    for hl in hyperlinks:
        print(f"{base_url}{hl}")

    manager.close()


if __name__ == "__main__":
    main()
