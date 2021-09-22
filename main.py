from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import envato_adapter
import db_adapter
import localization
import logging
from logentries import LogentriesHandler
from decouple import config

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
log.addHandler(LogentriesHandler(config('LOGENTRIES_TOKEN')))

updater = Updater(token=config('TELEGRAM_BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    lang = update.message.from_user.language_code
    message = localization.getWelcomeMessage(lang)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    log.info(f"User {getUserDataString(update)} has executed the start command")

dispatcher.add_handler(CommandHandler('start', start))

def getAccounts(update, context): 
    accounts = db_adapter.getAccountNames(update.effective_chat.id) 
    lang = update.message.from_user.language_code  
    message = '\n'.join(accounts) if len(accounts) > 0 else localization.getNoSubscriptionsFoundMessage(lang)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    log.info(f"User {getUserDataString(update)} has executed the get command")

dispatcher.add_handler(CommandHandler('get', getAccounts))

def readUserInput(update, context):
    userInput = update.message.text
    lang = update.message.from_user.language_code

    log.info(f"User {getUserDataString(update)} has executed \'{userInput}\' command")

    data = userInput.split(" ")

    if len(data) < 2:
        answer = localization.getIDontUnderstandYouMessage(lang)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        return

    command = data[0].lower()
    accountName = data[1]

    if command == 'add':
        addSubscription(context, update.effective_chat.id, accountName, lang)
    elif command == 'delete':
        deleteSubscription(context, update.effective_chat.id, accountName, lang)
    else:
        answer = localization.getIDontUnderstandYouMessage(lang)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

def addSubscription(context, chatId, accountName, lang):
    if envato_adapter.isUserExists(accountName):
        salesCount = envato_adapter.getSalesCountForUser(accountName)
        db_adapter.addOrUpdate(chatId, accountName, salesCount, lang)
        answer = localization.getAccountAddedMessage(lang, accountName)
    else:
        answer = localization.getAccountNotFoundMessage(lang, accountName)
    
    context.bot.send_message(chat_id=chatId, text=answer)

def deleteSubscription(context, chatId, accountName, lang):
    db_adapter.deleteSubscription(chatId, accountName)
    answer = localization.getAccountDeletedMessage(lang, accountName)
    context.bot.send_message(chat_id=chatId, text=answer)

dispatcher.add_handler(MessageHandler(Filters.text and ~Filters.command, readUserInput))

def checkSalesCount(update, context):
    log.info(f"User {getUserDataString(update)} has executed the check command")

    lang = update.message.from_user.language_code
    currentChatId = update.effective_chat.id

    accounts = db_adapter.getAccounts(currentChatId)

    for account in accounts:

        chatId = account["chatId"]
        accountName = account["accountName"]
        salesCount = account["salesCount"]

        newSalesCount = envato_adapter.getSalesCountForUser(accountName)

        if newSalesCount > salesCount:
            db_adapter.addOrUpdate(chatId, accountName, newSalesCount, lang)
            message = localization.getNewSaleMessage(lang, accountName, salesCount, newSalesCount)
            context.bot.send_message(chat_id=chatId, text=message)
        else:
            message = localization.getNoSalesMessage(lang, accountName)
            context.bot.send_message(chat_id=chatId, text=message)

dispatcher.add_handler(CommandHandler('check', checkSalesCount))   

def getUserDataString(update):
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    language_code = update.message.from_user.language_code

    return f"{first_name} {last_name} {username} {language_code}"
    
updater.start_polling()
updater.idle()