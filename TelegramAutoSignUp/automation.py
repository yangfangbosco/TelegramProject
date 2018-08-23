from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon import TelegramClient, sync
from telethon.errors import UserBannedInChannelError,SessionPasswordNeededError, PhoneNumberUnoccupiedError
from getpass import getpass
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import re
import csv
import asyncio
import random
import sys
import names

def get_number_from_yima():
    # return mobile, token, itemid
    username = 'yangfangdev'
    password = '111222'
    action = 'login'
    PARAMS = {'action':action, 'username':username, 'password':password}
    # Get the user token
    URL = "http://api.fxhyd.cn/UserInterface.aspx"
    response = requests.get(url = URL, params = PARAMS)
    result = response.text
    token = (result[8:])
    print(token)
    # Get the number
    action = 'getmobile'
    token = token
    itemid = '3988'
    PARAMS = {'action':action, 'token':token, 'itemid':itemid,'excludeno' : '171'}
    response = requests.get(url = URL, params = PARAMS)
    result = response.text
    mobile = (result[8:])
    #mobile = '17166922362'
    print(mobile)
    return mobile, token, itemid

def receive_msg(mobile,token,itemid):
    # return verify code
    URL = "http://api.fxhyd.cn/UserInterface.aspx"
    action = 'getsms'
    release = '0'
    PARAMS = {'action':action, 'token':token, 'itemid':itemid,'mobile':mobile,'release': release}
    response = requests.get(url = URL, params = PARAMS)
    times = 10;
    while((response.text == '3001') and times > 0):
        time.sleep(5)
        times = times - 1
        response = requests.get(url = URL, params = PARAMS)
        result = response.text
    result = response.text
    print(result)
    if('3001' in result):
        return 0
    m = re.search('code\sis\s(.+)', result)
    if m:
        code = m.group(1)
    else:
        print('error on code')
        sys.exit()
    print('the confirmation code is ' + str(code))
    return code

def signup(client,mobile, token, itemid,code):
    try:
        client.send_code_request('+(86)'+mobile)
        fname = names.get_first_name()
        lname = names.get_last_name()
        me = client.sign_up(code, fname, lname)
        print('signed up' + str(mobile))
        # breakpoint = input('enter 1 to continue: ')
        # more aciton
        client.edit_2fa(current_password=None, new_password='dataapplab', hint='', email=None)
        username = fname+lname+str(random.randint(1,10000))
        client(UpdateUsernameRequest(username))
        print('set password and username: ' + username)
        # breakpoint = input('enter 1 to continue: ')
        return username
    except Exception as e:
        print(str(e))
        quitprogram(client)

def quitprogram(client):
    client.log_out()
#sys.exit()

def checktelegramcode(client):
    print('check in the telegram code')
    try:
        telegramentity = client.get_entity(777000)
        for item in client.iter_messages(telegramentity,limit = 1):
            text = item.message
            print(text)
            if('confirmation code' in text):
                m = re.search('Telegram\swebsite\:\n(.+)', text)
                if m:
                    code = m.group(1)
                print('the confirmation code is ' + str(code))
            else:
                  m = re.search('login\scode\:\s(.+)', text)
                  if m:
                      code = m.group(1)
                  print('the confirmation code is ' + str(code))
        return code
    except Exception as e:
        client.log_out()
        print(str(e))


def generateapi(client,mobile):
    # breakpoint = input('please manully sign up for the web api and wait for code, enter 1 to continue: ')
    checktelegramcode(client)
    quitprogram(client)

def addnumbertoblacklist(mobile, token, itemid):
    URL = "http://api.fxhyd.cn/UserInterface.aspx"
    action = 'addignore'
    release = '1'
    PARAMS = {'action':action, 'token':token, 'itemid':itemid,'mobile':mobile}
    response = requests.get(url = URL, params = PARAMS)

def register_api(client, phone_number):
    driver = webdriver.Chrome()
    driver.get("https://my.telegram.org/auth")
    time.sleep(2)
    phone_area = driver.find_element_by_id("my_login_phone")
    phone_area.send_keys('+(86)'+phone_number)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(2)
    code_area = driver.find_element_by_id("my_password")
    time.sleep(10)
    code = input('enter telegram code: ')
    time.sleep(2)
    code_area.send_keys(code)
    time.sleep(2)
    driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    time.sleep(2)
    title = "dataapplab"+str(random.randint(1,10000))
    name = "datapp"+str(random.randint(1,10000))
    url = "https://my.telegram.org/apps"+str(random.randint(1,10000))
    driver.find_element_by_css_selector("div.my_main_content > ul > li > a").click()
    time.sleep(2)
    app_title = driver.find_element_by_id("app_title")
    app_title.send_keys(title)
    shortname = driver.find_element_by_id("app_shortname")
    shortname.send_keys(name)
    app_url = driver.find_element_by_id("app_url")
    app_url.send_keys(url)
    driver.find_element_by_xpath("//form[@id='app_create_form']/div[4]/div/div[6]/label")
    driver.find_element_by_id("app_save_btn").click()
    time.sleep(2)
    api_id = driver.find_element_by_xpath("//span[@onclick='this.select();']").text
    api_hash = driver.find_element_by_xpath("(//span[@onclick='this.select();'])[2]").text
    driver.find_element_by_css_selector("a.btn.btn-link").click()
    time.sleep(2)
    driver.find_element_by_xpath("//a[contains(text(),'Log out')]").click()
    print('api_id: ' + api_id)
    print('api_hash: ' + api_hash)
    return api_id, api_hash


def loginToTelegramonWeb(mobile, token, itemid):
    driver = webdriver.Chrome()
    driver.get("https://web.telegram.org/#/login")
    time.sleep(2)
    area = driver.find_element_by_name("phone_country")
    #this part can be updated by looping a phone book
    area.clear()
    area.send_keys("+86")
    time.sleep(2)
    phonenumber = driver.find_element_by_name("phone_number")
    #this part can be updated by looping a phone book
    phonenumber.send_keys(mobile)
    time.sleep(2)
    phonenumber.send_keys(u'\ue007')
    time.sleep(2)
    okbtn = driver.find_element_by_class_name("btn-md-primary")
    okbtn.send_keys(u'\ue007')
    time.sleep(2)
    code = receive_msg(mobile,token,itemid)
    print('the code is: ' + code)


client = TelegramClient('betpos'+str(random.randint(1,10000)), '406439', 'adca87612784c5419fe192015caf0ac5')
client.connect()
if not client.is_user_authorized():
    # breakpoint = input('enter 1 to continue: ')
    mobile, token, itemid = get_number_from_yima()
    try:
        sendcode = client.send_code_request('+(86)'+mobile)
    except Exception as e:
        if('banned' in str(e)):
            addnumbertoblacklist(mobile, token, itemid)
    code = receive_msg(mobile,token,itemid)
    print(code)
    print('is the number registered: ' + str(sendcode.phone_registered))
# breakpoint = input('enter 1 to continue: ')
    if(str(sendcode.phone_registered) == 'True'):
        print('This number has been registered, please sign_in, however, not implement ')
        quitprogram(client)
    else:
        print('This number has not been registered, please sign up')
        # breakpoint = input('enter 1 to continue: ')
        username = signup(client,mobile,token,itemid,code)
        # once finish signup, we should generate api
        client.log_out()
        time.sleep(20)
        loginToTelegramonWeb(mobile, token, itemid)
        # breakpoint = input('enter 1 to continue: ')
        api_id, api_hash = register_api(client, mobile)

        #now creating session phone, name, id, hash
        phone_number = mobile
        client_new = TelegramClient(str(mobile) + '_' + username+ '_'+ str(api_id)  +'_'+ str(api_hash), api_id, api_hash)
        client_new.connect()
        if not client_new.is_user_authorized():
            client_new.send_code_request('+(86)'+phone_number)
            try:
                code = input('enter telegram code: ')
                me = client_new.sign_in('+(86)'+phone_number, code)
                print('Done')
                print('+86'+str(mobile)+','+username+','+str(api_id)+','+str(api_hash))
                print(str(mobile)+'_'+username+'_'+str(api_id)+'_'+str(api_hash))
                quitprogram(client)
            
            except SessionPasswordNeededError:
                me = client_new.sign_in(password='dataapplab')
                print('Done')
                print('+86'+str(mobile)+','+username+','+str(api_id)+','+str(api_hash))
                print(str(mobile)+'_'+username+'_'+str(api_id)+'_'+str(api_hash))


            
        
        
















