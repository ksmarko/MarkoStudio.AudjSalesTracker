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