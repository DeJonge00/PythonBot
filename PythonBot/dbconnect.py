import constants, log, pymysql
from secret import secrets


# Welcome
def set_message(func_name: str, serverid: str, channelid: str, message: str):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "member_update", charset="utf8",
                           use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT serverID FROM {} WHERE serverID=%s".format(func_name), (serverid))
    t = c.fetchone()
    if t:
        if message:
            c.execute("UPDATE {} SET channelID=%s, message=%s WHERE serverID=%s".format(func_name),
                      (channelid, message, serverid))
        else:
            c.execute("DELETE FROM {} WHERE serverID=%s".format(func_name), (serverid))
    else:
        if message:
            c.execute("INSERT INTO {} VALUES (%s, %s, %s)".format(func_name), (serverid, channelid, message))
    conn.commit()
    conn.close()


def get_message(func_name: str, serverid: int):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "member_update")
    c = conn.cursor()
    c.execute("SELECT channelID, message FROM {} WHERE serverID=%s".format(func_name), (serverid))
    t = c.fetchone()
    conn.commit()
    conn.close()
    if t:
        return t
    return None


# Do not delete commands table
def get_do_not_delete_commands():
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "commands")
    c = conn.cursor()
    c.execute("SELECT serverid FROM do_not_delete_commands")
    t = c.fetchall()
    conn.commit()
    conn.close()
    if not t:
        return []
    return [str(x[0]) for x in t]


def set_do_not_delete_commands(serverids: [str]):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "commands")
    c = conn.cursor()
    c.execute("TRUNCATE TABLE do_not_delete_commands")
    for id in serverids:
        c.execute("INSERT INTO do_not_delete_commands VALUES (%s)", (id,))
    conn.commit()
    conn.close()


# Banned commands table
def get_banned_commands(type: str) -> dict:
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "commands")
    c = conn.cursor()
    c.execute("SELECT {0}id, command FROM {0}_banned_commands".format(type))
    t = c.fetchall()
    conn.commit()
    conn.close()
    if not t:
        return {}

    result = {}
    for identifier, command in t:
        result.setdefault(identifier, []).append(command)
    return result


def set_banned_commands(type: str, commands: {str: [str]}):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "commands")
    c = conn.cursor()
    c.execute("TRUNCATE TABLE {0}_banned_commands".format(type))
    for identifier in commands.keys():
        for command in commands.get(identifier):
            c.execute("INSERT INTO {0}_banned_commands VALUES (%s, %s)".format(type), (identifier, command))
    conn.commit()
    conn.close()
