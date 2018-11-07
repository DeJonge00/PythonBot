import common
from discord import Message

GENERAL_DATABASE = 'general'
WELCOME_TABLE = 'welcome'
GOODBYE_TABLE = 'goodbye'
DO_NOT_DELETE_TABLE = 'delete_comm'
BANNED_COMMANDS_TABLE = 'banned_comm'
PREFIX_TABLE = 'prefix'
SELF_ASSIGNABLE_ROLES_TABLE = 'selfassignable'
COMMAND_COUNTER_TABLE = 'count_comm'

SERVER_ID = 'serverid'
USER_ID = 'userid'
CHANNEL_ID = 'channelid'


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


# Do not delete commands table
def get_delete_commands(server_id: str):
    r = get_table(DO_NOT_DELETE_TABLE).find_one({SERVER_ID: server_id})
    return r.get('delete_commands', True) if r else True


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
    return get_table(PREFIX_TABLE).find_one({SERVER_ID: server_id}).get('prefix')


def set_prefix(server_id: str, prefix: str):
    get_table(PREFIX_TABLE).update({SERVER_ID: server_id}, {'$set': {'prefix': prefix}}, upsert=True)


# Command Counter
def command_counter(name: str, message: Message):
    get_table(COMMAND_COUNTER_TABLE).insert_one({
        'command': name,
        'timestamp': message.timestamp.timestamp(),
        'location': "{}/{}/{}".format(message.server.name, message.channel.name, message.author.name)
    })


# Self-assignable roles
def get_roles(server_id: str):
    r = get_table(SELF_ASSIGNABLE_ROLES_TABLE).find({SERVER_ID: server_id})
    return list(r) if r else []


def get_role(server_id: str, role_id: str):
    r = get_table(SELF_ASSIGNABLE_ROLES_TABLE).find_one({SERVER_ID: server_id})
    return r.get(role_id, False) if r else False


def toggle_role(server_id: str, role_id: str):
    v = not get_role(server_id, role_id)
    get_table(SELF_ASSIGNABLE_ROLES_TABLE).update({SERVER_ID: server_id}, {'$set': {role_id: v}}, upsert=True)
    return v
