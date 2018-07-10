from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon import TelegramClient
from time import sleep
import datetime
import csv
import sys
import pandas as pd
from ethnicolr import census_ln, pred_census_ln
import re
import logging
import mysql.connector
import urllib.parse
import requests
import json
import ngender
import gender_guesser.detector as gender


def is_chinese(string):
    """determine if the string contains chinese"""
    for uchar in string:
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
    return False
    
def is_arabic(string):
    """determine if the string contains arabic"""
    for uchar in string:
        if uchar >= u'\u0600' and uchar<=u'\u06FF':
            return True
    return False

def is_russian(string):
    """determine if the string contains russian"""
    for uchar in string:
        if uchar >= u'\u0400' and uchar<=u'\u04FF':
            return True
    return False

def is_korean(string):
    """determine if the string contains korean"""
    for uchar in string:
        if uchar >= u'\u3131' and uchar<=u'\uCB4C':
            return True
    return False

logging.basicConfig(filename='getUserName.log',level=logging.INFO)
logging.info("starting the get username program at "+ str(datetime.datetime.now()));

api_id = 251820
api_hash = '81cdef598d6d43d46cf6042c90bb6a7e'
client = TelegramClient('ClientIsExtractingUserFromThisGroup', api_id, api_hash)
phone_number = '+13015037867'

queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
all_participants = [["username","firstname","lastname","groupname","recordingTime","num_record","num_groupuser"]]
groupname = sys.argv[1]
channel = 'https://t.me/'  + groupname

print('we are in')
assert client.connect()
if not client.is_user_authorized():
    print('need to log in')
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Enter code: '))
print('start running')


count = 0
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
                    all_participants.append([user.username, user.first_name, user.last_name])
                    count = count+1;
                    print("1")

            except:
                print("error")
            
        # total += len(participants.users)
        offset += len(participants.users)

all_participants.append(["pleasedeletethisrow", "", "",groupname,str(datetime.datetime.now()),str(count),str(client.get_participants(channel,limit = 0).total)])
filename = channel[13:]  + '_user.csv'
myFile = open("tmp_"+filename, 'w',encoding="utf-8")
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(all_participants)
    
logging.info("ending the get username program at "+ str(datetime.datetime.now()));
logging.info("total: "+ str(count));
myFile.close;

#adding race prediction
logging.info("adding race prediction");
print("adding race prediction")
df = pd.read_csv("tmp_"+ filename, usecols=['username','firstname','lastname','groupname','recordingTime','num_record','num_groupuser'])
df = pd.DataFrame(df)
dict = {};
result = pred_census_ln(df, 'lastname')
result.to_csv(filename, sep=',')
logging.info("finished race prediction");
print("finished race prediction")
print(filename)

#f.write(str(datetime.datetime.now())+","+str(count)+","+str(client.get_participants(channel,limit = 0).total)+","+channel[13:])
#f.close()

#adding to database


#filename = "dx_chain_user_first.csv"
#groupname = "dxchain"


#connect to database
print("connecting db")



                            
cnx = mysql.connector.connect(user='root', password = '6666',
                              host='127.0.0.1',
                              database='telegram_test')  


  
print("db connected")                          
#get the cursor
cursor = cnx.cursor()
#parsing the input file
with open(filename, "r",encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
            userid = str(row[1])
            if(len(row)<=1):
                firstname = ""
                lastname = ""
            elif(len(row)<=2):
                firstname = str(row[2])
                lastname = ""
            else:
                firstname = str(row[2])
                lastname = str(row[3])
            fullname = firstname + lastname;
             #determine the eth    
            dict['api'] = row[9];
            dict['black'] = row[10];
            dict['hispanic'] = row[11];
            dict['white'] = row[12];
            def keyfunction(k):
               return dict[k]
            eth = [];
            for key in sorted(dict, key=keyfunction, reverse=True)[:4]:
                eth.append(key)
            #prepare the data and query
            # check Language of the name
            IsChinese = 0
            IsArabic = 0
            IsRussian = 0
            IsKorean = 0
            if(is_chinese(fullname)):
                IsChinese = 1;
                eth[0] = 'api';

                #check IsArabic
            elif(is_arabic(fullname)):
                IsArabic = 1;
                eth[0] = 'white'
                #check IsRussian
            elif(is_russian(fullname)):
                IsRussian = 1;
                eth[0] = 'white'
                #check IsKorean
            elif(is_korean(fullname)):
                IsKorean = 1;
                eth[0] = 'api' 

            if(lastname!=""):
                data = (userid,firstname,lastname,groupname,eth[0],eth[1],eth[2],eth[3],IsChinese, IsArabic, IsRussian, IsKorean)
            else:
                data = (userid,firstname,lastname,groupname,"","","","",IsChinese, IsArabic, IsRussian, IsKorean)
            query = ("INSERT INTO telegram_user(userID,Fname,Lname,GName,GetTimeStamp,E1,E2,E3,E4,IsChinese,IsArabic,IsRussian,IsKorean)"+
                    "VALUES(%s,%s,%s,%s,CURDATE(),%s,%s,%s,%s,%s,%s,%s,%s);") 
            print(query)
            print(data)
            #excuting  
            try:
                cursor.execute(query,data)
            except Exception as e:
                print("encounter an error, the error msg is the folloing:")
                print(e)
                pass
        
    
#commit the change
query = ("DELETE FROM telegram_user WHERE userID = 'pleasedeletethisrow'") 
cursor.execute(query)
cnx.commit()

#now update the gender

d = gender.Detector(case_sensitive=False)
print("updating gender info")

query = ("select id, Fname, Lname, IsChinese from telegram_user"+
    " where Gname= '" + groupname+"'")

cursor.execute(query)

row = cursor.fetchone()
runquery= [];
while(row!=None):
    try:
        row = cursor.fetchone()
        print(row)
        gender = ""
        if(int(row[3] == None or row[3]) != 0):
            fullname = str(row[1]) + str(row[2])
            result = ngender.guess(fullname)
            gender = result[0]
        else: 
            #name = (str(row[0])).encode("utf-8")
            result = d.get_gender(row[1])
            print(result)
            gender = result
            if(gender.find('male') != -1):
                gender = 'male'
            elif(gender.find('female') != -1):
                gender = 'female'
        runquery.append("update telegram_user set Gender = '" + str(gender) + "' where id = " + str(row[0]))
    except Exception as e:
        print("encounter an error, the error msg is the folloing:")
        print(e)
        pass;

for i in range(0,len(runquery)):
    print(runquery[i])
    cursor.execute(runquery[i])
print("done")
cnx.commit()

cursor.close()
cnx.close()




