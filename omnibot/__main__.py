"""
OmniBot

Some stupid joke bot I made for the sillies.

Also a test for better structured PyCord implementations.
"""
import json
from commands import bot

if __name__ == "__main__":    
    with open("token.json", "r") as f:
        bot.run(json.load(f)["token"])