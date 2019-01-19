from rpggame import rpgplayer
from database import rpg
import json

if __name__ == '__main__':
    with open('rpg_data_dump.json') as f:
        data = json.load(f)
    for p in data:
        p['userid'] = str(p.get('userid'))
        rpg.update_player(rpgplayer.dict_to_player(p))