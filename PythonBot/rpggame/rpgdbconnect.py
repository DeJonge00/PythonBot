import pymysql
from rpggame import rpgcharacter as rpgchar, rpgweapon as rpgw, rpgarmor as rpga
from secret import secrets


# Channels
def setRPGChannel(server_id: int, channel_id: str):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT channelID FROM rpgchannel WHERE serverID=%s", server_id)
    t = c.fetchone()
    if not t:
        c.execute("INSERT INTO rpgchannel VALUES ('{}', '{}')".format(server_id, channel_id))
    else:
        c.execute("UPDATE rpgchannel SET channelID={} WHERE serverID={}".format(channel_id, server_id))
    conn.commit()
    conn.close()


def getRPGChannel(server_id: str):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT channelID FROM rpgchannel WHERE serverID={}".format(server_id))
    t = c.fetchone()
    conn.commit()
    conn.close()
    if not t:
        print("Channel not specified for server")
        return None
    return t[0]


# Rpg
def getBusyPlayers():
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT playerID FROM busy WHERE busytime>0")
    t = c.fetchall()
    conn.commit()
    conn.close()
    players = {}
    for p in t:
        players[p[0]] = getPlayer(p[0])
    return players


def getPlayer(player_id: str):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT * FROM stats WHERE playerID={}".format(player_id))
    s = c.fetchone()
    c.execute("SELECT * FROM items WHERE playerID={}".format(player_id))
    i = c.fetchone()
    c.execute("SELECT * FROM busy WHERE playerID={}".format(player_id))
    b = c.fetchone()
    c.execute("SELECT * from weapon WHERE playerID={}".format(player_id))
    w = c.fetchone()
    c.execute("SELECT * from armor WHERE playerID={}".format(player_id))
    a = c.fetchone()
    conn.commit()
    conn.close()
    if not s:
        return rpgchar.RPGPlayer(player_id, str(player_id))
    player = rpgchar.RPGPlayer(player_id, str(player_id), role=s[1], health=s[2], maxhealth=s[3], damage=s[4], ws=s[5], critical=s[6])
    if i:
        player.exp = i[1]
        player.levelups = i[2]
        player.money = i[3]
        player.bosstier = i[4]
    if b:
        player.setBusy(b[3], b[1], b[2])
        player.kingtimer = b[4]
    if w:
        player.weapon = rpgw.RPGWeapon(w[1], w[2], w[3], w[4], w[5], w[6])
    if a:
        player.armor = rpga.RPGArmor(a[1], a[2], a[3], a[4], a[5], a[6])
    return player


def updatePlayers(stats: [rpgchar.RPGPlayer]):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB", charset="utf8", use_unicode=True)
    c = conn.cursor()
    try:
        for s in stats:
            if s.role is not rpgchar.DEFAULT_ROLE:
                if c.execute("SELECT playerID FROM stats WHERE playerID = {0}".format(s.userid)) == 0:
                    c.execute("INSERT INTO stats (playerID, role, health, maxhealth, damage, weaponskill, critical) VALUES (%s, %s, %s, %s, %s, %s, %s)", (s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill, s.critical))
                else:
                    c.execute("UPDATE stats SET role = %s, health = %s , maxhealth = %s, damage = %s, weaponskill = %s, critical = %s WHERE playerID = %s", (s.role, s.health, s.maxhealth, s.damage, s.weaponskill, s.critical, s.userid))
                if c.execute("SELECT playerID FROM items WHERE playerID = %s", s.userid) == 0:
                    c.execute("INSERT INTO items (playerID, exp, levelups, money, bosstier) VALUES (%s, %s, %s, %s, %s)", (s.userid, s.exp, s.levelups, s.money, s.bosstier))
                else:
                    c.execute("UPDATE items SET exp = %s, levelups = %s, money = %s, bosstier = %s WHERE playerID = %s", (s.exp, s.levelups, s.money, s.bosstier, s.userid))
                if c.execute("SELECT playerID FROM busy WHERE playerID = %s", s.userid) == 0:
                    c.execute("INSERT INTO busy (playerID, busytime, busychannel, busydescr, kingtimer) VALUES (%s, %s, %s, %s, %s)", (s.userid, s.busytime, s.busychannel, s.busydescription, s.kingtimer))
                else:
                    c.execute("UPDATE busy SET busytime = %s, busychannel = %s, busydescr=%s, kingtimer=%s WHERE playerID = %s", (s.busytime, s.busychannel, s.busydescription, s.kingtimer, s.userid))
                if c.execute("SELECT playerID FROM weapon WHERE playerID = %s", s.userid) == 0:
                    c.execute("INSERT INTO weapon (playerID, name, cost, element, damage, weaponskill, critical) VALUES (%s, %s, %s, %s, %s, %s, %s)", (s.userid, s.weapon.name, s.weapon.cost, s.weapon.element, s.weapon.damage, s.weapon.weaponskill, s.weapon.critical))
                else:
                    c.execute("UPDATE weapon SET name = %s, cost=%s, element=%s, damage=%s, weaponskill=%s, critical=%s WHERE playerID = %s", (s.weapon.name, s.weapon.cost, s.weapon.element, s.weapon.damage, s.weapon.weaponskill, s.weapon.critical, s.userid))
                if c.execute("SELECT playerID FROM armor WHERE playerID = %s", s.userid) == 0:
                    c.execute("INSERT INTO armor (playerID, name, cost, element, maxhealth, healthregen, money) VALUES (%s, %s, %s, %s, %s, %s, %s)", (s.userid, s.armor.name, s.armor.cost, s.armor.element, s.armor.maxhealth, s.armor.healthregen, s.armor.money))
                else:
                    c.execute("UPDATE armor SET name = %s, cost=%s, element=%s, maxhealth=%s, healthregen=%s, money=%s WHERE playerID = %s", (s.armor.name, s.armor.cost, s.armor.element, s.armor.maxhealth, s.armor.healthregen, s.armor.money, s.userid))
                conn.commit()
    except pymysql.err.InternalError as e:
        print(e)
    except pymysql.err.IntegrityError as e:
        print(e)
    finally:
        conn.close()


def getTopPlayers(group: str, amount: int):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT playerID, {0} FROM items ORDER BY {0} DESC LIMIT {1}".format(group, amount))
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a


def resetPlayers():
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("DELETE from items") 
    c.execute("DELETE from busy")
    c.execute("DELETE from rpgkings")
    c.execute("DELETE from weapon")
    c.execute("DELETE from armor")
    # Stats must be the last one
    c.execute("DELETE from stats")   
    conn.commit()
    conn.close()


def setKing(user_id, server_id):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    if c.execute("SELECT playerID FROM rpgkings WHERE serverID=%s", server_id) == 0:
        c.execute("INSERT INTO rpgkings (serverID, playerID) VALUES (%s, %s)", (server_id, user_id))
    else:
        c.execute("UPDATE rpgkings SET playerID = %s WHERE serverID = %s", (user_id, server_id))
    conn.commit()
    conn.close()


def getKing(server_id):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT playerID FROM rpgkings WHERE serverID=%s", server_id)
    king = c.fetchone()
    conn.commit()
    conn.close()
    return king[0] if king else None


def isKing(user_id):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    r = c.execute("SELECT serverID FROM rpgkings WHERE playerID=%s ", user_id)
    conn.commit()
    conn.close()
    return False if r == 0 else True


# Pats
def incrementPats(patter_id: str, pattee_id: str):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "PATS")
    c = conn.cursor()
    c.execute("SELECT patsNbr FROM pats_counters WHERE patterID=%s AND patteeID=%s", (patter_id, pattee_id))
    pats = c.fetchone()
    if pats:
        pats = pats[0]+1
        c.execute("UPDATE pats_counters SET patsNbr=%s WHERE patterID=%s AND patteeID=%s", (pats, patter_id, pattee_id))
    else:
        pats = 1
        c.execute("INSERT INTO pats_counters VALUES (%s, %s, %s)", (patter_id, pattee_id, pats))
    conn.commit()
    conn.close()
    return pats

