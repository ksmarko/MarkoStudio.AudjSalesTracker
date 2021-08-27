import redis
from decouple import config

db = redis.from_url(config('DB_CONNECTION_STRING'))

def addOrUpdate(chatId, accountName, salesCount):
    key = f"{chatId}:{accountName}"
    value = salesCount
    db.set(key, value)

def getAccounts(currentChatId):
    accounts = []
    all_keys = db.keys(pattern=f"{currentChatId}:*")

    for key in all_keys:

        data = key.decode("UTF-8").split(':')

        chatId = data[0]
        accountName = data[1]
        salesCount = db.get(key).decode("UTF-8")

        accounts.append({
            "chatId": chatId,
            "accountName": accountName,
            "salesCount": int(salesCount)
        })
    
    return accounts

def getAccountNames(chatId):
    accounts = []
    all_keys = db.keys(f"{chatId}:*")

    for key in all_keys:

        data = key.decode("UTF-8").split(':')

        accountName = data[1]
        accounts.append(accountName)

    return accounts

def deleteSubscription(chatIdToDelete, accountNameToDelete):
    all_keys = db.keys(pattern=f"{chatIdToDelete}:{accountNameToDelete}")
    for key in all_keys:
        db.delete(key)