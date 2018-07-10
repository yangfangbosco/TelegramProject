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


update_id = None
arr_text = ["Interesting!", "\U000026C4", "\U00002600"]

def main():
    logging.basicConfig(filename='FormSubmitterMoniterBot.log',level=logging.INFO)

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
            recordFormSubmittedUser(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def recordFormSubmittedUser(bot):
    """Echo the message the user sent."""
    global update_id;
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, limi=100, timeout=10):
        update_id = update.update_id + 1
        print(update.message);
        if(update.message.text!=None and (update.message.text.find("completed all the step")!=-1)):
            if(update.message.from_user.username!=None):
                logging.info(update.message.from_user.username + " completed all the step")
                logging.info(str(update.message)+"\n");
                update.message.reply_text("Thank you for completed all the airdrop step!")
                print(update.message.from_user.username);
                file = open('document.csv','a')
                file.write(update.message.from_user.username +"\n")
                file.close;
            else:
                logging.info("no user name")
                logging.info(str(update.message)+"\n");

                    
if __name__ == '__main__':
    main()