# arb-search

Arbitrage betting is rare, but possible with the right tools and intuition. This is a fool-proof method of making money off of sports betting no matter what team wins. In this project, I scour various sports books to see if there are any current arbitrage opportunities. Then, a user can see if there are any arbitrage opportunities with respect to the bets they made in the past. Finally, I use time series forecasting to predict how a team's odds will change (go up or down), which may be useful in determining arbitrage betting opportunities.

Here are the skills I refined:
- Web scraping. I have only done web scraping once in the past, and for this project, I had to figure out a way to web-scrape baseball win probabilities off of ESPN. This task was daunting and frustrating at first, but I was able to accomplish this after researching common web scraping tactics, including Beautiful Soup 4.

- Database design. I have worked with MongoDB before, but this was my first main project in SQL. I was always very comfortable with NoSQL databases, but once I realized information on odds was relational, I knew I needed to use a SQL database. I used the Python sqlite to collect data and organize it. I'm glad I was able to familiarize myself with SQL databases and also use a MongoDB database to hold other information.

- Forecasting techniques. Forecasting sounds scary and seems complicated. The math seems difficult, but once you find its derivations from standard regression tactics, it's not too bad. I learned about Arima and Prophet models, and most importantly, that data science requires experimenting with various models to see what truly sticks. On top of this, being organized with data, design, and visualizations can make it far easier to replicate such processes down the line, when training on new data sets.

Overall skills: data science (forecasting), sklearn, SQL.

## To Do
- [ ] Move schemas and interfaces to a dedicated location