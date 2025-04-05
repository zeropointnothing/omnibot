import json
from commands import bot

if __name__ == "__main__":    
    with open("token.json", "r") as f:
        bot.run(json.load(f)["token"])