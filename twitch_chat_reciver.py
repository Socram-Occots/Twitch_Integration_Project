# twitch_chat_reciver
# This file takes chat logs from twitch.tv/m0ng0n and analyzes them
#
# Leared from this: 
# https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
#
#imports
import socket
import logging
from emoji import demojize
from datetime import datetime
import re
import pandas as pd
import csv 
import threading
import sys
import os

sock = socket.socket()
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'Mongon'
token = 'oauth:1mp5k0btjh7dci0klpsxdzg5k65g3b'
channel = '#m0ng0n'

escaper = None
infile = None

# creating log file
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s — %(message)s',
                datefmt='%Y-%m-%d_%H:%M:%S',
                handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

def main():

    escape_route_thread = threading.Thread(target = escape_route)
    escape_route_thread.start()
    initialize_csv_file()
    sock_to_twitch()
    recieving_twitchchat_thread = threading.Thread(target = receivingtwitchchat)
    recieving_twitchchat_thread.start()

    

def sock_to_twitch():
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))


def receivingtwitchchat():
    global escaper
    while True:
        resp = sock.recv(2048).decode('utf-8')
        print(resp) # remove print
            
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
            
        elif len(resp) > 0:
            logging.info(demojize(resp))
            
        sorting_each_chat(resp)
            

def initialize_csv_file():
    global infile
    try:
        infile = open('mongon_chat_history.csv', 'r', encoding='UTF8')
    except FileNotFoundError:
         infile = open('mongon_chat_history.csv', 'w', encoding='UTF8')
         headers = ['dt', 'channel', 'username', 'message']
         dfchat = pd.DataFrame(columns = headers)
         dfchat.to_csv('mongon_chat_history.csv', index=False)
    


def sorting_each_chat(resp):
    header = ['dt', 'channel', 'username', 'message']
    with open("chat.log", 'r', encoding='utf-8') as f:
          lines = f.read().split('\n\n\n')
    for line in lines:
        try:
            time_logged = line.split('—')[0].strip()
            time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

            username_message = line.split('—')[1:]
            username_message = '—'.join(username_message).strip()

            username, channel, message = re.search(
                ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
            ).groups()
            
            d = {'dt': time_logged, 'channel': channel, 'username': username, 'message': message}
            with open('mongon_chat_history.csv', 'a', newline='', encoding='utf-8') as file:

                writer = csv.DictWriter(file, fieldnames = header)
                writer.writerow(d)  
        except Exception:
            pass


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
