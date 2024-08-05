# MLB Game Predictor Workflow

This directory contains a series of scripts designed to load webpages, extract MLB game URLs, and predict game matchups. The workflow is tied together using a bash script to automate the process.

## Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [webpage_loader.py](#webpage_loaderpy)
  - [get_mlb_game_urls.py](#get_mlb_game_urlspy)
  - [get_mlb_game_matchup_predictor.py](#get_mlb_game_matchup_predictorpy)
  - [collect_mlb_predictions.sh](#collect_mlb_predictionssh)

## Overview

1. **webpage_loader.py**: Loads webpages using a WebDriver.
2. **get_mlb_game_urls.py**: Uses the webpage loader to feed the source into a web scraper which grabs all the URLs for the upcoming MLB games and writes them to a file.
3. **get_mlb_game_matchup_predictor.py**: Grabs the matchup prediction for a given game given its URL.
4. **collect_mlb_predictions.sh**: Bash script that ties all of this together and writes the results to a text file.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- WebDriver (Ensure the `WEBDRIVER` environment variable is set)
- WebDriver Type (Ensure the `WEBDRIVER_TYPE` environment variable is set)
- Bash

## Usage
### Notes

Before executing the scripts, ensure that the following environment variables are set:

- `WEBDRIVER`: The path to your WebDriver executable (e.g., ChromeDriver).
- `WEBDRIVER_TYPE`: The type of WebDriver you are using (e.g., `chrome`).

Set the environment variables in your shell:

```bash
export WEBDRIVER="/path/to/your/webdriver"
export WEBDRIVER_TYPE="chrome"
```