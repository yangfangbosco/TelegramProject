

import logging
from telethon.tl.functions.channels import InviteToChannelRequest
import asyncio
from telethon import TelegramClient
import time
from requests import get
import datetime
import csv

async def main():
    #print('we are in the read function')
    global startingline
    logging.info("connecting")
    
    assert client.connect()
    if not client.is_user_authorized():
        #print('need to log in')
        try:
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter code: '))
        except:
            print("enter code problem, process next api")
            logging.info("enter code problem, process next api")
            startingline -= 40
            return
    
    logging.info("current number of group members is " + str(client.get_participants(channel, limit = 0).total) + "\n")
    logging.info("start adding from " + str(startingline))
    print("start testing from " + str(startingline))

    pre_count = client.get_participants(channel, limit = 0).total

    try:
        client(InviteToChannelRequest(channel, users_to_add[startingline: startingline+10]))
    except:
        print("flood error")
        logging.error("current api is flooded")

    updated_count = client.get_participants(channel, limit = 0).total

    if(updated_count - pre_count < 4):
        print("You can't add person now")
        logging.error("You can't add person now")
        startingline -= 40
    else:
        startingline += 10
        print("testing success, finished at " + str(startingline))
        logging.info("testing success, finished at " + str(startingline))
        round = 1;
        #if(preTest(startingline) == false):
            #pass
        for ii in range(startingline, startingline+40, 20):
            try:
                start = time.clock()
                #print('working on round ' + str(round))
                logging.info('working on round ' + str(round))
                print('working on round ' + str(round))
                logging.info("adding from " + str(ii));
                print("adding from " + str(ii))
                
                client(InviteToChannelRequest(channel, users_to_add[ii: ii+20]))
                
                logging.info('finished round ' + str(round))
                print('finished round ' + str(round))
                logging.info("finished at " + str(ii+20));
                print("finished at " + str(ii+20))
                end = time.clock()
                
                round = round + 1;
                #print('take a rest of 30 seconds')
                
                time.sleep(10)
                
            except:
                #print('current api exhasuted, use next one')
                logging.error("current api exhausted");
                #logging.info(sys.exc_info()[0])
                print("current api exhausted")
                logging.info(str(datetime.datetime.now()));
                print(str(datetime.datetime.now()))
                
                ii -= 20;
                
                time.sleep(10)
    
    logging.info("this api has finished\n")
    logging.info("after adding, current number of the group members is " + str(client.get_participants(channel, limit = 0).total) + "\n")        
             
'''
def preTest(startingline):
    pre_count = client.get_participants(channel, limit = 0).total
    client(InviteToChannelRequest(channel, users_to_add[startingline: startingline+1]))
    updated_count = client.get_participants(channel, limit = 0).total
    if(updated_count - pre_count != 1):
        return false
    else:
        return true
        startingline += 1
'''


# starting the program
# get the logger ready
logging.basicConfig(filename='addMembers.log',level=logging.INFO)
logging.info("starting the add member program at "+ str(datetime.datetime.now()));
print("starting the add member program at "+ str(datetime.datetime.now()))
#print("starting the add member program at "+ str(datetime.datetime.now()))

ip = get('https://api.ipify.org').text
logging.info("My public IP address is:" + str(ip) + "\n\n")
print("My public IP address is:" + str(ip))
#print("My public IP address is:" + str(ip))

# read the output file from index.js
with open("testoutput.txt", "r") as f:
    users_to_add = [ii.strip() for ii in f.readlines()]
    
# determine the starting line of username file
#startingline = argv[1];
startingline = 8400
    
# read the input user file
    
with open(<your file>,"r",encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        logging.info("processing" + str(row["ID"]))
        print("\n\n"+"processing" + str(row["ID"]))
        #setting api id hash and phone number channel
        api_id = row["API_ID"]
        api_hash = row["API_Hash"]
        phone_number = row["Phone"]
        print(str(row["Phone"]))
        channel = 'https://t.me/Detrust'<channel>
        #start running the loop
        loop = asyncio.get_event_loop()
        
        client = TelegramClient('mym8787'+str(row["API_ID"]), api_id, api_hash)
        
        loop.run_until_complete(main())
        startingline = startingline + <starting line>
        logging.info("next time we will start from " + str(startingline) + "\n")
       
