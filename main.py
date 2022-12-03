import src.game as game
import json

def getJsonSettings():
    with open('settings.json', mode='r') as f:
        settings = json.load(f)
        f.close()
    
    return settings

if __name__ == '__main__':
    game.Game(getJsonSettings())
