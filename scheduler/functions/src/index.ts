import * as functions from "firebase-functions";
import * as Redis from "ioredis";
const request = require('requestretry');
const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN);
const redis = new Redis(9564, process.env.DB_HOST_NAME);

export const scheduledFunction = functions.pubsub.schedule('every 10 mins').onRun(async context => {
    redis.keys('*', (err: any, keys: any[]) => {    

        if (err) {
            return functions.logger.error(err.message);
        }

        keys.forEach((key: string) => {
            redis.get(key).then((result) => {

                let data = key.split(':');
                let chatId = data[0];
                let accountName = data[1];
                let splittedResult = result.split(':');
                let salesCount = Number(splittedResult[0]);
                let lang = splittedResult[1];

                let options = {
                    url: `https://api.envato.com/v1/market/user:${accountName}.json`,
                    headers: {
                      'Authorization': `Bearer ${process.env.ENVATO_KEY}`
                    },
                    json: true,
                    maxAttempts: 5,
                    retryDelay: 1000, // 1 second
                  };
                
                request(options, function (err, res, body) {
                    
                    if (err) {
                        return functions.logger.error(err.message);
                    }

                    if (res && res.attempts > 1) {
                        functions.logger.warn('The number of request attempts: ' + res.attempts);
                    }

                    // if user not found
                    if (body.error !== undefined) {
                        return functions.logger.error(body.error);
                    }

                    let newSalesCount = body.user.sales;

                    functions.logger.info(`Sales count = ${salesCount}, new sales count = ${newSalesCount}`);
            
                    if (newSalesCount > salesCount) {
                        functions.logger.info(`New sale for user ${accountName}! Previous sales count: ${salesCount}, new sales count: ${newSalesCount}. ChatId = ${chatId}`);
                        
                        redis.set(`${chatId}:${accountName}`, `${newSalesCount}:${lang}`);
                        
                        let message = lang == 'uk' || lang == 'ru'
                            ? `💰💰💰 Нова продажа для ${accountName}! К-сть продаж до: ${salesCount}, к-сть продаж зараз: ${newSalesCount}. Переходь за посиланням https://audiojungle.net/user/${accountName}/statement щоб переглянути деталі`
                            : `💰💰💰 New sale for user ${accountName}! Previous sales count: ${salesCount}, new sales count: ${newSalesCount}. Go to https://audiojungle.net/user/${accountName}/statement to see more`;
                        bot.sendMessage(chatId, message);
                    }
                    else {
                        functions.logger.info(`No new sales for user ${accountName}. ChatId = ${chatId}`);
                    }
                }).end();
            }, error => {
                functions.logger.error('Error occurred', error);
            });
        });
    });
  });