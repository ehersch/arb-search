import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date

# This code downloads the CSV from https://www.rotowire.com/baseball/injury-report.php

# Setup Chrome options to handle downloads
chrome_options = webdriver.ChromeOptions()
download_dir = "/Users/ethanhersch/independent-code/arb-search/data"  # Change this to your download directory
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True,
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.rotowire.com/baseball/injury-report.php")

try:
    # Wait until the button is present and clickable, then click it
    download_button_xpath = '//*[@id="injury-report"]/div[3]/div[2]/button[2]'
    download_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, download_button_xpath))
    )
    print("Download button found. Clicking the button.")
    download_button.click()

    # Wait for the download to complete (adjust the waiting time if necessary)
    print("Waiting for the download to complete.")
    WebDriverWait(driver, 2).until(
        lambda driver: any(
            [fname.endswith(".csv") for fname in os.listdir(download_dir)]
        )
    )
    print("CSV file downloaded successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
