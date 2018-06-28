import constants, log, pymysql
from secret import secrets


# Welcome
def set_message(func_name: str, serverid: str, channelid: str, message: str):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "member_update", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT serverID FROM {} WHERE serverID=%s".format(func_name), (serverid))
    t = c.fetchone()
    if t:
        if message:
            c.execute("UPDATE {} SET channelID=%s, message=%s WHERE serverID=%s".format(func_name), (channelid, message, serverid))
        else:
            c.execute("DELETE FROM {} WHERE serverID=%s".format(func_name), (serverid))
    else:
        if message:
            c.execute("INSERT INTO {} VALUES (%s, %s, %s)".format(func_name), (serverid, channelid, message))
    conn.commit()
    conn.close()


def get_message(func_name: str, serverid : int):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "member_update")
    c = conn.cursor()
    c.execute("SELECT channelID, message FROM {} WHERE serverID=%s".format(func_name), (serverid))
    t = c.fetchone()
    conn.commit()
    conn.close()
    if t:
        return t
    return None
