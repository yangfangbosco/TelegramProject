#!/usr/bin/env python
# -*- coding: utf-8 -*-



"""Simple Bot to reply to Telegram messages.

This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import random
import datetime


update_id = None
arr_text = ["Interesting!", "\U000026C4", "\U00002600"]

def main():
    logging.basicConfig(filename='system.log',level=logging.INFO)
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(#add your own bot token)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        bot.get_updates();
    except IndexError:
        update_id = None

    #logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            autoReply(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def autoReply(bot):
    """Echo the message the user sent."""
    global update_id;
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, limi=100, timeout=10):
        update_id = update.update_id + 1
        logging.info(str(datetime.datetime.now()));
        logging.info(str(update.message)+"\n");
        #skip message that a minute ago
        if update.message.date >= datetime.datetime.now() - datetime.timedelta(0,60):
            #welcome
            #print(update.message);
            print(update.message);
            if(len(update.message.new_chat_members)!=0):
                bot.send_message(chat_id=update.message.chat.id, text="Welcome to our group!",parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                #process the chat message
                #Keyword: airdrop
                if(update.message.text!=None and 
                   (update.message.text.find("airdrop")!=-1
                   or update.message.text.find("空投")!=-1
                   or update.message.text.find("糖果")!=-1
                   or update.message.text.find("空头")!=-1
                   or update.message.text.find("공중 투하")!=-1)):
                    response = "Get Detrust token XTD airdrop on http://detrustairdrop.com"
                    update.message.reply_text(response);
               
                else:
                    number = random.randint(1,100);
                    #print(update.message)
                    #print(number);
                    if(number < 20):
                        index = random.randint(0,len(arr_text)-1)
                        bot.send_message(chat_id=update.message.chat.id, text=arr_text[index],parse_mode=telegram.ParseMode.MARKDOWN)
                    
if __name__ == '__main__':
    main()