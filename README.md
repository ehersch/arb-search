# arb-search

Here you will find a few major files where code and such is located.

Right now, the data directory contains an MLB injury report CSV, and a JSON odds1.json.

There are a few other files here but those are unimportant and will eventually be deleted.

I plan on storing this data in Mongo in the future, as this is better when we collect a lot of data.
For now, these files can be found here bacause they are being used for testing.

Inside src, there are 2 directories: cols and logic.

Cols (or "collections") contains a script api.py to get a json of all of the sports odds from our odds API.
The file injuries.py performs the webscraping to get baseball injury data in a CSV.
Then parse_json.py takes the json fro api.py and essentially extracts the relevant data for our purposes
and then stores this as a new json in data. test.json is what we use for testing

Logic contains code for the various service offered by this program. For example, enter_bets.py allows a
user to enter their previous bets into a database, and find_bets.py is used to pull previous bets on a
certain game. Then, find_arb parses through the odds posted on each matchup to find if there is an
arbitrage opporutnity available.

Finally,src/main.py is what the user interacts with. Through the command line they indicate here which service
they want to take advantage of. They can search for a current arbitrage opportunities (either bases off of
live odds on both sides ot odds on one team versus odds from a bet they already places). They can enter their
previous bets. Finally, they can take advantage of the odds forecaster and use this to predict if there
will be a future arbitrage opportunity.
