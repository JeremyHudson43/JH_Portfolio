# HudsonRepo
Hello, and welcome to my GitHub. I've written the following programs for fun and to practice my programming skills. My work is organized by folder, please read below for more information. 

## Python

### Interactive Brokers (IBKR) Stock Trading Bot
``IBKR Stock Trading Bot`` - My most recent project -- A Python-based trading bot that interacts with Interactive Brokers' API. The bot utilizes a mean reversion indicator called Connor's RSI, using one of two choices:

1.) A daily timeframe for individual stocks, buying at market open and selling before market close

2.) A shorter timeframe (5-30 minutes) for options trading. Poitions are only held for a few minutes, so it can be volatile. 

The bot is automated, but user intervention is required for initial setup and for making adjustments to trading parameters. Be sure to read and understand the risk disclosure before live trading.

### GPT-4 Stock Predictions for SPY
``GPT-4 Stock Predictions`` - A Python script that uses OpenAI's GPT-4 language model to generate one-day stock predictions for the SPY ETF and emails these predictions to a specified list of recipients. This script requires your own OpenAI API key to generate the predictions and a SMTP setup for sending the emails. 

Due to the inherent uncertainty of stock market predictions, this tool is intended for educational and entertainment purposes only.

## Java Swing
``Library Management System`` - A detailed project that simulates functions of a librarian. These include check-in, check out, managing customers, and looking up and maintaining books. Implements the Google Books API and a local MySQL database. 

This project was designed as part of a group project, but the code I wrote is clearly labeled at the top of each Java file. A more detailed description can be found under docs inside the Library Management System folder. 

## SQL / PHP
``Sample Company Database`` - Simulates a simple company database implementing SQL and using PHP as a backend for CRUD operations.

## C++
``WAR - Card Game`` - This is a fun C++ project where I've implemented a classic card game, War. This is a text-based game that simulates a two-player game of War, with a human player and an AI opponent. Each round, the game will deal a card to each player from a virtual deck, with the player having the highest card winning the round. 
