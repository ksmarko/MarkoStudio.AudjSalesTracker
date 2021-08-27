from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import envato_adapter
import db_adapter
import logging
from logentries import LogentriesHandler
from decouple import config

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
log.addHandler(LogentriesHandler(config('LOGENTRIES_TOKEN')))

updater = Updater(token=config('TELEGRAM_BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    message = f'😎 Welcome to the AudioJungle Sales Tracker bot! 😎\n\n' + '❓ What can this bot do?\n\n' + '📌 Text me \'Add account_name\', and I will check this account every 10 minutes for the new sales and notify you.\nIf you want to add another account for checking - just text me again. I will check them all.\n\n📌 If you want to delete some account from the check list - text me \'Delete account_name\' and I won\'t check for it anymore\n\n📌 If you want to check sales manually - just send me the /check command\n\n📌 If you want to see all subscriptions - send me the /get command'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    log.info(f"User {getUserDataString(update)} has executed the start command")

dispatcher.add_handler(CommandHandler('start', start))

def getAccounts(update, context): 
    accounts = db_adapter.getAccountNames(update.effective_chat.id)    
    message = '\n'.join(accounts)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    log.info(f"User {getUserDataString(update)} has executed the get command")

dispatcher.add_handler(CommandHandler('get', getAccounts))

def readUserInput(update, context):
    userInput = update.message.text

    log.info(f"User {getUserDataString(update)} has executed \'{userInput}\' command")

    data = userInput.split(" ")

    if len(data) < 2:
        answer = 'I don\'t understand you. Available commands are \'Add account_name\' and \'Delete account_name\''
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        return

    command = data[0].lower()
    accountName = data[1]

    if command == 'add':
        addSubscription(context, update.effective_chat.id, accountName)
    elif command == 'delete':
        deleteSubscription(context, update.effective_chat.id, accountName)
    else:
        answer = 'I don\'t understand you. Available commands are \'Add account_name\' and \'Delete account_name\''
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

def addSubscription(context, chatId, accountName):
    if envato_adapter.isUserExists(accountName):
        salesCount = envato_adapter.getSalesCountForUser(accountName)
        db_adapter.addOrUpdate(chatId, accountName, salesCount)
        answer = f'✅ Account {accountName} added to the check list'
    else:
        answer = f'❗️ Account {accountName} not found'
    
    context.bot.send_message(chat_id=chatId, text=answer)

def deleteSubscription(context, chatId, accountName):
    db_adapter.deleteSubscription(chatId, accountName)
    answer = f'🗑 Account {accountName} deleted from the check list'
    context.bot.send_message(chat_id=chatId, text=answer)

dispatcher.add_handler(MessageHandler(Filters.text and ~Filters.command, readUserInput))

def checkSalesCount(update, context):

    log.info(f"User {getUserDataString(update)} has executed the check command")

    currentChatId = update.effective_chat.id

    accounts = db_adapter.getAccounts(currentChatId)

    for account in accounts:

        chatId = account["chatId"]
        accountName = account["accountName"]
        salesCount = account["salesCount"]

        newSalesCount = envato_adapter.getSalesCountForUser(accountName)

        if newSalesCount > salesCount:
            db_adapter.addOrUpdate(chatId, accountName, newSalesCount)
            message = f"💰💰💰 New sale for user ${accountName}! Previous sales count: ${salesCount}, new sales count: ${newSalesCount}. Go to https://audiojungle.net/user/${accountName}/statement to see more"
            context.bot.send_message(chat_id=chatId, text=message)
        else:
            message = f"😕 No new sales for user {accountName}"
            context.bot.send_message(chat_id=chatId, text=message)

dispatcher.add_handler(CommandHandler('check', checkSalesCount))   

def getUserDataString(update):
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username

    return f"{first_name} {last_name} {username}"
    
updater.start_polling()
updater.idle()