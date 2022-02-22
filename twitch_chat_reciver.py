# twitch_chat_reciver
# This file takes chat logs from twitch.tv/m0ng0n and analyzes them
#
# Leared from this: 
# https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
#
#imports
import socket
sock = socket.socket()
import logging
from emoji import demojize
from datetime import datetime
import re
import pandas as pd


server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'Mongon'
token = 'oauth:1mp5k0btjh7dci0klpsxdzg5k65g3b'
channel = '#m0ng0n'

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




    sock_to_twitch()
    #loggingtwitchchat()
    receivingtwitchchat()
    


def sock_to_twitch():
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))


def receivingtwitchchat():
    while True:
        resp = sock.recv(2048).decode('utf-8')
        print(resp) #
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
    
        elif len(resp) > 0:
            logging.info(demojize(resp))

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

                username, channel, message = re.search(
                    ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
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
