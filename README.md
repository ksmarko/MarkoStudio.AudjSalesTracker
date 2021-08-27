# About
This is a Telegram bot that checks the AudioJungle account sales count every 10 minutes and notifies users about new sales. Bot username: @audj_sales_tracker_bot

What can this bot do?

- Text me 'Add account_name', and I will check this account every 10 minutes for the new sales and notify you.
If you want to add another account for checking - just text me again. I will check them all.

- If you want to delete some account from the check list - text me 'Delete account_name' and I won't check for it anymore

- If you want to check sales manually - just send me the /check command

- If you want to see all subscriptions - send me the /get command

## Project parts:
1. Scheduled function
2. Telegram bot

## Scheduled function
Written in Node.js 14
Hosted on Firebase

Readme here https://github.com/ksmarko/MarkoStudio.AudjSalesTracker/blob/master/scheduler/README.md

## Telegram Bot
Written in Python 3.9
Hosted on Heroku

Run script locally: python main.py

Packages:
pip install redis
pip install requests
pip install python-telegram-bot

Or run command `pip install -r requirements.txt`

Всё, о чём должен знать разработчик Телеграм-ботов: https://habr.com/ru/post/543676/ \n

Deploy bot to Heroku:
1. Create requirements.txt file
2. Create Procfile
3. push to master on GitHub
4. Heroku -> Create app -> Deploy -> GitHub -> Resources -> Enable worker

Source: https://medium.com/tech-insights/how-to-deploy-a-python-script-or-bot-to-heroku-in-5-minutes-a82de2d3ed40
