from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon import TelegramClient
from time import sleep
import datetime

import re
import logging

logging.basicConfig(filename='getUserName.log',level=logging.INFO)
logging.info("starting the get username program at "+ str(datetime.datetime.now()));

api_id = <your api id>
api_hash = <your api hash>
client = TelegramClient(<your client name>, api_id, api_hash)
phone_number = <your phone number>

queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
all_participants = []
channel = 'https://t.me/MediLOTOfficial'<channel>

print('we are in')
assert client.connect()
if not client.is_user_authorized():
    print('need to log in')
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Enter code: '))
print('start running')


for key in queryKey:
    offset = 0
    limit = 100
    while True:
        participants = client(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(key), offset, limit,
            hash=0
        ))
        
        if not participants.users:
            break
        for user in participants.users:
            try:
	            if re.findall(r"\b[a-zA-Z]", user.username)[0].lower() == key:
	                all_participants.append(user.username + "," + user.first_name + "," + user.last_name)
	                print("1")

            except:
                print("error")
            
        # total += len(participants.users)
        offset += len(participants.users)

f = open(channel[13:] + " " + 'user.txt', 'w')
count = 0
for name in all_participants:
	f.write(name+"\n")
	count = count + 1
print(count)

f.write(str(datetime.datetime.now())+","+str(count)+","+str(client.get_participants(channel,limit = 0).total)+","+channel[13:])
f.close()

logging.info("ending the get username program at "+ str(datetime.datetime.now()));
logging.info("total: "+ str(count));