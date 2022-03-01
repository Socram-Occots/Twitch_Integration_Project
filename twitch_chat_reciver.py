# twitch_chat_reciver
# This file takes chat logs from twitch.tv/m0ng0n and analyzes them
#
# Leared from this: 
# https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
#
#imports
from glob import escape
import socket
sock = socket.socket()
import logging
from emoji import demojize
from datetime import datetime
import re
import pandas as pd
import csv 
import threading


server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'Mongon'
token = 'oauth:1mp5k0btjh7dci0klpsxdzg5k65g3b'
channel = '#m0ng0n'

escape = None

# creating log file
logging.basicConfig(level=logging.DEBUG,
                 format='%(asctime)s — %(message)s',
                 datefmt='%Y-%m-%d_%H:%M:%S',
                handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

def main():
    '''df = get_chat_dataframe('chat.log')
    df.set_index('dt', inplace=True)
    print(df)
    df.head()'''

    initialize_csv_file()
    sock_to_twitch()
    #loggingtwitchchat()
    recieving_twitchchat_thread = threading.Thread(target = receivingtwitchchat)
    escape_route_thread = threading.Thread(target = escape_route, args=escape)

    recieving_twitchchat_thread.start()
    escape_route_thread.start()

    


def sock_to_twitch():
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))


def receivingtwitchchat():
    while escape != "Y":
        resp = demojize(
            sock.recv(2048).decode('utf-8')
        )
        
        print(resp) # remover print
        
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        sorting_each_chat(resp)
    '''
        elif len(resp) > 0:
            logging.info(demojize(resp))
            '''

        
        


def initialize_csv_file():
    try:
        open('mongon_chat_history.csv', 'r', encoding='UTF8')
    except Exception:
        open('mongon_chat_history.csv', 'w', encoding='UTF8')


def sorting_each_chat(resp):
    header = ['dt', 'channel', 'username', 'message']

    time_logged = resp.split('—')[0].strip()
    time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

    username_message = resp.split('—')[1:]
    username_message = '—'.join(username_message).strip()

    username, channel, message = re.search(
          ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
    ).groups()

    d = {'dt': time_logged, 'channel': channel, 'username': username, 'message': message}
    with open('mongon_chat_history.csv', 'a', newline='', encoding='utf-8') as file:

        writer = csv.DictWriter(file, fieldnames = header)
        writer.writerow(d)



def escape_route(escape):
    while escape != "Y":
        escape = str(input("Exit now? Enter \'Y\': ")).strip()

   

'''
def get_chat_dataframe(file):
     data = []
     with open(file, 'r', encoding='utf-8') as f:
          lines = f.read().split('\n\n\n')
          
        for line in lines:
            try:
                 time_logged = line.split('—')[0].strip()
                 time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')
                  username_message = line.split('—')[1:]
                    username_message = '—'.join(username_message).strip()
                    username, channel, message = re.search(                        ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
                 ).groups()
                    d = {
                        'dt': time_logged,
                        'channel': channel,
                        'username': username,
                        'message': message
                    }
                    data.append(d)
                                except Exception:
                    pass
                
    return pd.DataFrame().from_records(data)     
    '''

       

#def loggingtwitchchat():
#   logging.info(receivingtwitchchat.resp)


"""time_log = resp.split(" ")[0].strip()
    print(time_log)
    time_log = datetime.strptime(time_log, '%Y-%m-%d_%H:%M:%S')
    print(time_log)
    username_message = msg.split('—')[1:]
    username_message = '—'.join(username_message).strip()
    username, channel, message = re.search
        (':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message).groups()
    """



main()
