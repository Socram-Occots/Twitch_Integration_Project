# twitch_chat_reciver.py
# This file takes chat logs from twitch.tv/m0ng0n and stores them
#
# Learned from this: 
# https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
#
#imports
import socket
from emoji import demojize
from datetime import datetime
import pytz
import re
import pandas as pd
import csv 
import threading
import sys
import os
import requests
import win32gui, win32con

# hiding python terminal
min = win32gui.GetForegroundWindow()
win32gui.ShowWindow(min , win32con.SW_MINIMIZE)

# setting gobal variables
sock = socket.socket()
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'Mongon'
token = None
channel = '#m0ng0n'

# grabbing private api POST link and stream chat oath ticket
try:
    with open(r"C:\Users\socra\Documents\git-hut_stuff\DO_NOT_CLONE_THIS_FILE\authtickets.txt","r") as file:
        lines = file.readlines()
        token = lines[0]
        resplink = lines[1]
except Exception as e:
    print(e)

infile = None
escaper = None
csvpath = r"C:\Users\socra\Documents\git-hut_stuff\twitch_interaction_sesaw_project\Twitch_Integration_Project\mongon_chat_history.csv"

# main execution
def main():
    #escape_route_thread = threading.Thread(target = escape_route)
    #escape_route_thread.start()
    initialize_csv_file()
    sock_to_twitch()
    

# connecting to twitch on  a loop until success
def sock_to_twitch():
    while True:
        try:
            sock.connect((server, port))

            sock.send(f"PASS {token}\n".encode('utf-8'))
            sock.send(f"NICK {nickname}\n".encode('utf-8'))
            sock.send(f"JOIN {channel}\n".encode('utf-8'))
            break
        except Exception as ConnectionResetError:
            print("Connection Error... Retrying...\n")

    # starting twitch chat collection
    receivingtwitchchat()
    

# receives twitch chat
def receivingtwitchchat():
    while True:
        resp = sock.recv(2048).decode('utf-8').strip()
        print(resp) # remove print     

        # sorts twitch chat and stores it into csv file and onine server
        sorting_each_chat(resp)
    

# opening csv file to store chat in locally
def initialize_csv_file():
    global infile
    try:
        infile = open(csvpath, 'r', encoding='UTF8')
    except FileNotFoundError:
         infile = open(csvpath, 'w', encoding='UTF8')
         headers = ['dt', 'channel', 'username', 'message']
         dfchat = pd.DataFrame(columns = headers)
         dfchat.to_csv(csvpath, index=False)
    


# sorting twitch chat into 4 categories the storing in locally and online
def sorting_each_chat(resp):
    header = ['dt', 'channel', 'username', 'message']
    try:

        # Chicago time zone for dating chat
        tz_CH = pytz.timezone('America/New_York') 
        datetime_CH = datetime.now(tz_CH)
        time_logged = datetime_CH.strftime("%Y-%m-%d_%H:%M:%S")

        username, channel, message = re.search(
            ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp
        ).groups()
        
        d = {'dt': time_logged, 'channel': channel, 'username': username, 'message': message}
    
        # sending dict in string form to server
        post = requests.post(resplink, data = str(d))

        # checking post success
        print(post)

        # appending dict to local csv file
        with open(csvpath, 'a', newline='', encoding='utf-8') as file:

            writer = csv.DictWriter(file, fieldnames = header)
            writer.writerow(d)  
    except Exception as e:
        pass
        

# extra loop for debugging. 
# This method seems to lag the program when running so it is commented out by default
def escape_route():
    global infile
    global escaper
    global sock
    while escaper != "Y":
        escaper = str(input("Exit now? Enter \'Y\': \n")).strip()
    sock.close()
    infile.close()
    os._exit(os.X_OK)


main()
