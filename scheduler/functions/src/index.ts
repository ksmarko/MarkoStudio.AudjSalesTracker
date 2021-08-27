import * as functions from "firebase-functions";
import * as Redis from "ioredis";
import * as request from "request";
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
                let salesCount = Number(result);

                let options = {
                    url: `https://api.envato.com/v1/market/user:${accountName}.json`,
                    headers: {
                      'Authorization': `Bearer ${process.env.ENVATO_KEY}`
                    },
                    json: true
                  };
                
                request(options, function (err, res, body) {
                    
                    if (err) {
                        return functions.logger.error(err.message);
                    }

                    // if user not found
                    if (body.error !== undefined) {
                        return functions.logger.error(body.error);
                    }

                    let newSalesCount = body.user.sales;
            
                    if (newSalesCount > salesCount) {
                        functions.logger.info(`New sale for user ${accountName}! Previous sales count: ${salesCount}, new sales count: ${newSalesCount}. ChatId = ${chatId}`);
                        redis.set(`${chatId}:${accountName}`, newSalesCount);
                        let message = `💰💰💰 New sale for user ${accountName}! Previous sales count: ${salesCount}, new sales count: ${newSalesCount}. Go to https://audiojungle.net/user/${accountName}/statement to see more`;
                        bot.sendMessage(chatId, message);
                    }
                    else {
                        functions.logger.info(`No new sales for user ${accountName}. ChatId = ${chatId}`);
                    }
                }).end();
            });
        });
    });
  });