import database.common as common
from discord import Message, Server, Channel

GENERAL_DATABASE = 'general'
WELCOME_TABLE = 'welcome'
GOODBYE_TABLE = 'goodbye'
DO_NOT_DELETE_TABLE = 'delete_comm'
BANNED_COMMANDS_TABLE = 'banned_comm'
PREFIX_TABLE = 'prefix'
SELF_ASSIGNABLE_ROLES_TABLE = 'selfassignable'
COMMAND_COUNTER_TABLE = 'count_comm'
STARBOARD_CHANNEL_TABLE = 'starchannels'
STARBARD_MESSAGES_TABLE = 'starmessages'
SERVER_TABLE = 'servers'
CHANNEL_TABLE = 'channels'

SERVER_ID = 'serverid'
USER_ID = 'userid'
CHANNEL_ID = 'channelid'
MESSAGE_ID = 'messageid'


def get_table(table):
    return common.get_table(GENERAL_DATABASE, table)


# Welcome
def set_message(table: str, server_id: str, channel_id: str, message: str):
    get_table(table).update({SERVER_ID: server_id}, {'$set': {CHANNEL_ID: channel_id, 'message': message}}, upsert=True)


def get_message(table: str, server_id: str):
    r = get_table(table).find_one({SERVER_ID: server_id})
    if not r:
        return None, None
    return r.get('channelid', None), r.get('message', None)


# Starboard
def set_star_channel(server_id: str, channel_id: str):
    table = get_table(STARBOARD_CHANNEL_TABLE)
    table.update({SERVER_ID: server_id}, {'$set': {CHANNEL_ID: channel_id}}, upsert=True)


def get_star_channel(server_id: str):
    r = get_table(STARBOARD_CHANNEL_TABLE).find_one({SERVER_ID: server_id})
    if not r:
        print("Starboard channel not specified for server")
        return None
    return r.get(CHANNEL_ID) if r else None


def get_star_message(message_id: str):
    r = get_table(STARBARD_MESSAGES_TABLE).find_one({MESSAGE_ID: message_id}, {'embed_id': 1})
    return r.get('embed_id') if r else None


def update_star_message(message_id: str, embed_id: str):
    get_table(STARBARD_MESSAGES_TABLE).update_one({MESSAGE_ID: message_id}, {'$set': {'embed_id': embed_id}},
                                                  upsert=True)


# Do not delete commands table
def get_delete_commands(server_id: str):
    r = get_table(DO_NOT_DELETE_TABLE).find_one({SERVER_ID: server_id})
    return r.get('delete_commands', True) if r else True


def set_delete_commands(server_id: str, state: bool):
    get_table(DO_NOT_DELETE_TABLE).update({SERVER_ID: server_id}, {'$set': {'delete_commands': state}}, upsert=True)


def toggle_delete_commands(server_id: [str]):
    v = not get_delete_commands(server_id)
    get_table(DO_NOT_DELETE_TABLE).update({SERVER_ID: server_id}, {'$set': {'delete_commands': v}}, upsert=True)
    return v


# Banned commands table
def get_banned_command(id_type: str, iden: str, command: str):
    r = get_table(BANNED_COMMANDS_TABLE).find_one({id_type: iden})
    return r.get(command, False) if r else False


def toggle_banned_command(id_type: str, iden: str, command: str):
    v = not get_banned_command(id_type, iden, command)
    get_table(BANNED_COMMANDS_TABLE).update({id_type: iden}, {'$set': {command: v}}, upsert=True)
    return v


# Prefix
def get_prefix(server_id: str):
    r = get_table(PREFIX_TABLE).find_one({SERVER_ID: server_id})
    return r.get('prefix') if r else None


def set_prefix(server_id: str, prefix: str):
    get_table(PREFIX_TABLE).update({SERVER_ID: server_id}, {'$set': {'prefix': prefix}}, upsert=True)


# Command Counter
def command_counter(name: str, message: Message):
    if message.server:
        server = message.server.name
    else:
        server = "Direct Message"
    get_table(COMMAND_COUNTER_TABLE).insert_one({
        'command': name,
        'timestamp': message.timestamp.timestamp(),
        'server': server,
        'channel': message.channel.name,
        'author': message.author.name
    })


# Self-assignable roles
def get_roles(server_id: str):
    r = get_table(SELF_ASSIGNABLE_ROLES_TABLE).find_one({SERVER_ID: server_id})
    return [i for i in r.keys() if r[i] == True] if r else []


def get_role(server_id: str, role_id: str):
    r = get_table(SELF_ASSIGNABLE_ROLES_TABLE).find_one({SERVER_ID: server_id})
    return r.get(role_id, False) if r else False


def toggle_role(server_id: str, role_id: str):
    v = not get_role(server_id, role_id)
    get_table(SELF_ASSIGNABLE_ROLES_TABLE).update({SERVER_ID: server_id}, {'$set': {role_id: v}}, upsert=True)
    return v


# Bot information
def server_as_dict(s: Server):
    return {
        'name': s.name,
        SERVER_ID: s.id,
        'members': s.member_count,
        'bots': len([x for x in s.members if x.bot]),
        'icon': s.icon_url,
        'channels': {
            'text': [c.id for c in s.channels if str(c.type) == 'text'],
            'voice': [c.id for c in s.channels if str(c.type) == 'voice']
        }
    }


def channel_as_dict(c: Channel):
    return {
        'name': c.name,
        CHANNEL_ID: c.id,
        'type': str(c.type)
    }


def update_server_list(servers: [Server]):
    server_table = get_table(SERVER_TABLE)
    channel_table = get_table(CHANNEL_TABLE)
    for s in servers:
        server_table.replace_one({SERVER_ID: s.id}, server_as_dict(s), upsert=True)
        for c in s.channels:
            if str(c.type) in ['text', 'voice']:
                channel_table.replace_one({CHANNEL_ID: c.id}, channel_as_dict(c), upsert=True)
