#!/bin/bash
python3 get_mlb_game_urls.py --url https://www.espn.com/mlb/schedule --headless --wait_class_names "ScheduleTables" > mlb_game_urls.txt

# Read each line from the file and pass it to the python script
while IFS= read -r url
do
    python3 get_mlb_game_matchup_predictor.py --url "$url" --headless --wait_class_names "matchupPredictor" >> match_predictions.txt
done < mlb_game_urls.txt
