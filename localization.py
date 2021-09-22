en = 'en'
ua = 'uk'
ru = 'ru'

def getWelcomeMessage(languageCode):
    if (isFromUkraine(languageCode)):
        message = '''
😎 Привіт від AudioJungle Sales Tracker bot! 😎
❓ Чим можу бути корисним?
💡 Якщо тобі лінь перевіряти кількість продаж на своєму аккаунті AudioJungle самостійно - ти можеш довірити це мені. Я буду перевіряти його кожні 10 хв і відпишу тобі, коли хтось щось купить
📌 Щоб додати аккаунт в список перевірки - напиши мені Add account_name, де account_name - це назва аккаунта, для якого треба перевіряти к-сть продаж. Якщо ти хочеш перевіряти декілька аккаунтів - повтори команду
📌 Якщо ти раптом передумаєш перевіряти продажі якогось аккаунта, то виключити його зі списку перевірки можна відправивши повідомлення Delete account_name
📌 Щоб отримати список всіх аккаунтів, які я буду для тебе перевіряти, надішли мені команду /get
📌 А якщо тобі хочеться перевірити всі свої аккаунти тут і зараз, то відправ мені команду /check і я відпишу, чи були нові продажі з моменту останньої перевірки
🤟 Що б ти не написав, я завжди відповім на твої повідомлення, але якщо раптом я мовчу - то щось пішло не так і краще звернутися за допомогою до @kseniia_marko'''

    else:
        message = '''
😎 Welcome to the AudioJungle Sales Tracker bot! 😎
❓ What can this bot do?
📌 Text me \'Add account_name\', and I will check this account every 10 minutes for the new sales and notify you. For example, you can text me \'Add EliteMusic\' and I will add the \'EliteMusic\' account to the check list and will notify you about new sales
If you want to add another account for checking - just text me again. I will check them all.
📌 If you want to delete some account from the check list - text me \'Delete account_name\' and I won\'t check for it anymore
📌 If you want to check sales manually - just send me the /check command
📌 If you want to see all subscriptions - send me the /get command
🤟 No matter what you write, I will always respond to your messages. But if suddenly I am silent  - it means that something went wrong and it's better to ask @kseniia_marko for help'''

    return message

def getNoSubscriptionsFoundMessage(languageCode):
    if (isFromUkraine(languageCode)):
        message = 'Ти не додав жодного аккаунта для перевірки к-сті продаж, щоб додати надішли мені Add account_name, де account_name - назва аккаунту, для якого ти хочеш перевіряти продажі'
    else:
        message = 'You don\'t have any subscriptions, text me Add account_name to add. account_name is a name of the AudioJungle account you want to check sales for'
    
    return message

def getIDontUnderstandYouMessage(languageCode):
    if (isFromUkraine(languageCode)):
        message = '''
Не розумію тебе 😶
📌 Щоб додати аккаунт в мій список перевірки - напиши мені Add account_name, де account_name - це назва аккаунта, для якого треба перевіряти к-сть продаж. Якщо ти хочеш перевіряти декілька аккаунтів - повтори команду, я буду перевіряти їх всі
📌 Якщо ти раптом передумаєш перевіряти продажі якогось аккаунта, то виключити його із мого списку перевірки можна відправивши повідомлення Delete account_name
📌 Щоб отримати список всіх аккаунтів, які я буду для тебе перевіряти, надішли мені команду /get
📌 А якщо тобі хочеться перевірити всі свої аккаунти тут і зараз, то відправ мені команду /check і я відпишу тобі, чи були нові продажі з моменту останньої перевірки
'''
    else:
        message = '''
I don\'t understand you 😶 
📌 Text me \'Add account_name\' if you want to add new account to the check list 
📌 Text me \'Delete account_name\' if you want to delete the account_name account from the check list
📌 If you want to check sales manually - just send me the /check command
📌 If you want to see all subscriptions - send me the /get command
'''

    return message

def getAccountAddedMessage(languageCode, accountName):
    if (isFromUkraine(languageCode)):
        message = f'✅ Аккаунт {accountName} додано до списку перевірки'
    else:
        message = f'✅ Account {accountName} added to the check list'
    
    return message

def getAccountNotFoundMessage(languageCode, accountName):
    if (isFromUkraine(languageCode)):
        message = f'❗️ Аккаунт {accountName} не знайдено на AudioJungle'
    else:
        message = f'❗️ AudioJungle account {accountName} not found'
    
    return message

def getAccountDeletedMessage(languageCode, accountName):
    if (isFromUkraine(languageCode)):
        message = f'🗑 Аккаунт {accountName} видалено зі списку перевірки'
    else:
        message = f'🗑 Account {accountName} deleted from the check list'
    
    return message

def getNewSaleMessage(languageCode, accountName, salesCount, newSalesCount):
    if (isFromUkraine(languageCode)):
        message = f"💰💰💰 Нова продажа для ${accountName}! К-сть продаж до: ${salesCount}, к-сть продаж зараз: ${newSalesCount}. Переходь за посиланням https://audiojungle.net/user/${accountName}/statement щоб переглянути деталі"
    else:
        message = f"💰💰💰 New sale for user ${accountName}! Previous sales count: ${salesCount}, new sales count: ${newSalesCount}. Go to https://audiojungle.net/user/${accountName}/statement to see more"
    
    return message

def getNoSalesMessage(languageCode, accountName):
    if (isFromUkraine(languageCode)):
        message = f"😕 Жодної нової продажі для {accountName}"
    else:
        message = f"😕 No new sales for user {accountName}"
    
    return message

def isFromUkraine(languageCode):
    return languageCode == ua or languageCode == ru