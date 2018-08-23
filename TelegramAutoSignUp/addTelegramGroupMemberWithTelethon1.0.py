import logging
from telethon.tl.functions.channels import InviteToChannelRequest
import asyncio
from telethon import TelegramClient,sync
from telethon.errors import UserBannedInChannelError, FloodWaitError, ChatWriteForbiddenError,SessionPasswordNeededError
import time
from requests import get
import datetime
import csv
from getpass import getpass

def main():
    #print('we are in the read function')
    global startingline
    logging.info("connecting")
    
    client.connect()

    if not client.is_user_authorized():
        #print('need to log in')
        try:
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter code: '))
        except SessionPasswordNeededError:
            pw = getpass('Two step verification is enabled. '
                         'Please enter your password: ')
            me = client.sign_in(password=pw)
        except:
            print("enter code problem, process next api")
            logging.info("enter code problem, process next api")
            startingline -= 40
            return
    current_num = client.get_participants(channel, limit = 0).total
    logging.info("current number of group members is " + str(current_num) + "\n")
    print("current number of group members is " + str(current_num) + "\n")
    logging.info("start adding from " + str(startingline))
    print("start testing from " + str(startingline))

    pre_count = client.get_participants(channel, limit = 0).total

    flag = preTest(startingline)

    while flag:
        flag = preTest(startingline)
        startingline += 10

    updated_count = client.get_participants(channel, limit = 0).total

    if(updated_count - pre_count < 1):
        print("You can't add person now")
        logging.error("You can't add person now")
    else:
        startingline += 10
        print("testing success, finished at " + str(startingline))
        logging.info("testing success, finished at " + str(startingline))
        round = 1;
        #if(preTest(startingline) == false):
            #pass
        round_count = client.get_participants(channel, limit = 0).total
        while (round_count - updated_count < 40 and round < 7):
            try:
                start = time.clock()
                #print('working on round ' + str(round))
                logging.info('working on round ' + str(round))
                print('working on round ' + str(round))
                logging.info("adding from " + str(startingline));
                print("adding from " + str(startingline))
                
                client(InviteToChannelRequest(channel, users_to_add[startingline: startingline+20]))
                
                logging.info('finished round ' + str(round))
                print('finished round ' + str(round))
                logging.info("finished at " + str(startingline+20));
                print("finished at " + str(startingline+20))
                end = time.clock()
                
                round = round + 1;
                #print('take a rest of 30 seconds')
                
                time.sleep(10)
                round_count = client.get_participants(channel, limit = 0).total
                startingline += 20

            except:
                #print('current api exhasuted, use next one')
                logging.error("current api exhausted");
                #logging.info(sys.exc_info()[0])
                print("current api exhausted")
                logging.info(str(datetime.datetime.now()));
                print(str(datetime.datetime.now()))
                
                startingline += 20
                round = round + 1
                time.sleep(10)
        '''
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
        '''
    logging.info("this api has finished\n")
    after_num = client.get_participants(channel, limit = 0).total
    logging.info("after adding, current number of the group members is " + str(after_num) + "\n")
    print("after adding, current number of the group members is " + str(after_num) + "\n")        
             

def preTest(startingline):
    userflag = False

    try:
        client(InviteToChannelRequest(channel, users_to_add[startingline: startingline+10]))
    except FloodWaitError as e:
        print("flood error")
        logging.error("current api is flooded")
    except UserBannedInChannelError as e:
        print("User Banned In Channel error")
        logging.error("current api is banned")
    except ChatWriteForbiddenError as e:
        print("Chat Write forbidden error")
        logging.error("Chat Write forbidden error")
    except:
        print("unknown error from " + str(startingline))
        logging.error("unknown error")
        userflag = True

    return userflag


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
users_to_add = []
with open("huobiofficial_user.csv", "r") as f:
    '''
    for ii in f.readlines():
        line = ii.split(',')
        users_to_add.append(line[0].strip())
    '''
    reader = csv.DictReader(f)
    for row in reader:
        users_to_add.append(row["username"])
print(users_to_add)

# determine the starting line of username file
#startingline = argv[1];
startingline = 20080
    
# read the input user file
   
with open("api.csv","r",encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        logging.info("processing" + str(row["ID"]))
        print("\n\n"+"processing" + str(row["ID"]))
        #setting api id hash and phone number channel
        api_id = row["API_ID"]
        api_hash = row["API_Hash"]
        phone_number = row["Phone"]
        print(str(row["Phone"]))
        print(row["Name"])
        channel = 'https://t.me/calculusnetwork'
        #start running the loop
        
        client = TelegramClient('17029424056_MichaelCloud7505_433478_fd0b4bd36bb590835178521e1a1a5d12', api_id, api_hash)
        main()

        logging.info("next time we will start from " + str(startingline) + "\n")

       
