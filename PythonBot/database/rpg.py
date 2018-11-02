import pymongo

from database.common import get_table as get_database_and_table
from rpgplayer import RPGPlayer, dict_to_player, BUSY_DESC_BOSSRAID, BUSY_DESC_NONE
import rpgconstants as rpgc

RPG_DATABASE = 'rpg'
CHANNEL_ID = 'channelid'
SERVER_ID = 'serverid'
USER_ID = 'userid'

RPG_CHANNEL_TABLE = 'rpg_channel'
RPG_PLAYER_TABLE = 'rpg_player'
RPG_KING_TABLE = 'rpg_king'


def get_table(table):
    return get_database_and_table(RPG_DATABASE, table)


# Channels
def set_rpg_channel(server_id: str, channel_id: str):
    table = get_table(RPG_CHANNEL_TABLE)
    table.update({SERVER_ID: server_id}, {'$set': {CHANNEL_ID: channel_id}}, upsert=True)


def get_rpg_channel(server_id: str):
    r = get_table(RPG_CHANNEL_TABLE).find({SERVER_ID: server_id})
    if not r:
        print("Channel not specified for server")
        return None
    return r[0].get(CHANNEL_ID)


# Rpg
def get_player(player_id: str, player_name: str):
    r = list(get_table(RPG_PLAYER_TABLE).find({USER_ID: player_id}))
    return dict_to_player(r[0]) if r else RPGPlayer(userid=player_id, username=player_name)


def get_busy_players(busydesc):
    return [(x.get('userid'), x.get('busy')) for x in get_table(RPG_PLAYER_TABLE).find({'busy.description': busydesc})]


def get_done_players():
    return get_table(RPG_PLAYER_TABLE).find({'busy.time': 0})


def update_player(player: RPGPlayer):
    get_table(RPG_PLAYER_TABLE).replace_one({USER_ID: player.userid}, player.as_dict(), upsert=True)


def reset_busy(user_id: str):
    get_table(RPG_PLAYER_TABLE).update(
        {USER_ID: user_id},
        {'$set':
            {'busy':
                {
                    'time': 0,
                    'channel': 0,
                    'description': BUSY_DESC_NONE
                }}})


def decrement_busy_counters():
    get_table(RPG_PLAYER_TABLE).update_many({'busy.description': {'$not': {'$eq': BUSY_DESC_NONE}}},
                                            {'$inc': {'busy.time': -1}})


def do_health_regen():
    t = get_table(RPG_PLAYER_TABLE)
    r = t.find({'stats.health': {'$lt': 'stats.maxhealth'}})
    if not r:
        return
    for player in r:
        if player.get('busy').get('description') == BUSY_DESC_NONE:
            percentage = 0.025 if player.get('role') == rpgc.names.get('role')[4][0] else 0.01
        else:
            percentage = 0.05 if player.get('role') == rpgc.names.get('role')[4][0] else 0.03
        health = min(player.get('stats').get('maxhealth'), player.get('stats').get('maxhealth') * (1 + percentage))
        t.update({USER_ID: player.get(USER_ID)}, {'stats.health': health})


def add_stats(playerid: str, stat: str, amount: int):
    get_table(RPG_PLAYER_TABLE).update({USER_ID: playerid}, {'$inc': {stat: amount}})


def add_pet_stats(playerid: str, stat: str, amount: int):
    for x in range(len(list(get_table(RPG_PLAYER_TABLE).find({USER_ID: playerid}))[0].get('pets', []))):
        get_table(RPG_PLAYER_TABLE).update({USER_ID: playerid}, {'$inc': {'pets.{}.{}'.format(x, stat): amount}})


def get_top_players(group: str, start: int, amount: int):
    ps = get_table(RPG_PLAYER_TABLE).find().sort(group, pymongo.ASCENDING).skip(start).limit(amount)
    return [(x.get('stats').get('name'), x.get(group)) for x in ps]


def get_boss_parties():
    r = get_table(RPG_PLAYER_TABLE).find({'busy.description': BUSY_DESC_BOSSRAID})
    res = {}
    for item in [dict_to_player(x) for x in r]:
        res.setdefault(item.busychannel, []).append(item)
    return res


def set_king(user_id: str, server_id: str):
    get_table(RPG_KING_TABLE).update({SERVER_ID: server_id}, {'$set': {USER_ID: user_id}})


def get_king(server_id: str):
    r = get_table(RPG_KING_TABLE).find({SERVER_ID: server_id})
    return r[0] if r else None


def is_king(user_id: str):
    return bool(get_table(RPG_KING_TABLE).find({USER_ID: user_id}))
