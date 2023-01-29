import pyautogui
import tempfile
import random

screenshot = pyautogui.screenshot()
screenshot.save(tempfile.gettempdir() + '/abc-' + str(random.randint(0, 1000)) + ".png")