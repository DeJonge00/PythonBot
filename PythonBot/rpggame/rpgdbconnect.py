import asyncio, discord, constants, log, pickle, removeMessage, pymysql
from rpggame import rpgweapon as rpgw, rpgarmor as rpga
from discord.ext import commands
from secret import secrets
from rpggame import rpgcharacter as rpgchar

# Channels
def setRPGChannel(serverid : int, channelid : int):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT channelID FROM rpgchannel WHERE serverID={}".format(serverid))
    t = c.fetchone()
    if t == None:
        c.execute("INSERT INTO rpgchannel VALUES ('{}', '{}')".format(serverid, channelid))
    else:
        c.execute("UPDATE rpgchannel SET channelID={} WHERE serverID={}".format(channelid, serverid))
    conn.commit()
    conn.close()

def getRPGChannel(serverid : str):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT channelID FROM rpgchannel WHERE serverID={}".format(serverid))
    t = c.fetchone()
    conn.commit()
    conn.close()
    if t==None:
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

def getPlayer(playerid):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT * FROM stats WHERE playerID={}".format(playerid))
    s = c.fetchone()
    c.execute("SELECT * FROM items WHERE playerID={}".format(playerid))
    i = c.fetchone()
    c.execute("SELECT * FROM busy WHERE playerID={}".format(playerid))
    b = c.fetchone()
    c.execute("SELECT * from tierboss WHERE playerID={}".format(playerid))
    t = c.fetchone()
    c.execute("SELECT * from weapon WHERE playerID={}".format(playerid))
    w = c.fetchone()
    c.execute("SELECT * from armor WHERE playerID={}".format(playerid))
    a = c.fetchone()
    conn.commit()
    conn.close()
    if s == None:
        return rpgchar.RPGPlayer(playerid, str(playerid))
    player = rpgchar.RPGPlayer(playerid, str(playerid), role=s[1], health=s[2], maxhealth=s[3], damage=s[4], ws=s[5], critical=s[6])
    if i != None:
        player.exp = i[1]
        player.levelups = i[2]
        player.money = i[3]
    if b != None:
        player.setBusy(b[3], b[1], b[2])
    if t != None:
        player.bosstier = t[1]
    if w != None:
        player.weapon = rpgw.RPGWeapon(w[1], w[2], w[3], w[4], w[5], w[6])
    if a != None:
        player.armor = rpga.RPGArmor(a[1], a[2], a[3], a[4], a[5], a[6])
    return player

def updatePlayers(stats : [rpgchar.RPGPlayer]):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    try:
        for s in stats:
            #stats
            if c.execute("SELECT playerID FROM stats WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO stats (playerID, role, health, maxhealth, damage, weaponskill, critical) VALUES ({0}, '{1}', {2}, {3}, {4}, {5}, {6})".format(s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill, s.critical))
            else :
                c.execute("UPDATE stats SET role = '{1}', health = {2} , maxhealth = {3}, damage = {4}, weaponskill = {5}, critical = {6} WHERE playerID = {0}".format(s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill, s.critical))        
            #items
            if c.execute("SELECT playerID FROM items WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO items (playerID, exp, levelups, money) VALUES ({}, {}, {}, {})".format(s.userid, s.exp, s.levelups, s.money))
            else :
                c.execute("UPDATE items SET exp = {}, levelups = {}, money = {} WHERE playerID = {}".format(s.exp, s.levelups, s.money, s.userid))
            #busy
            if c.execute("SELECT playerID FROM busy WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO busy (playerID, busytime, busychannel, busydescr) VALUES ({0}, {1}, '{2}', '{3}')".format(s.userid, s.busytime, s.busychannel, s.busydescription))
            else :
                c.execute("UPDATE busy SET busytime = {1}, busychannel = '{2}', busydescr ='{3}' WHERE playerID = {0}".format(s.userid, s.busytime, s.busychannel, s.busydescription))
            #tierboss
            if c.execute("SELECT playerID FROM tierboss WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO tierboss (playerID, bosstier) VALUES ({0}, {1})".format(s.userid, s.bosstier))
            else :
                c.execute("UPDATE tierboss SET bosstier = {1} WHERE playerID = {0}".format(s.userid, s.bosstier))
            #weapon
            if c.execute("SELECT playerID FROM weapon WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO weapon (playerID, name, cost, element, damage, weaponskill, critical) VALUES ({}, \"{}\", {}, {}, {}, {}, {})".format(s.userid, s.weapon.name, s.weapon.cost, s.weapon.element, s.weapon.damage, s.weapon.weaponskill, s.weapon.critical))
            else :
                c.execute("UPDATE weapon SET name = \"{}\", cost={}, element={}, damage={}, weaponskill={}, critical={} WHERE playerID = {}".format(s.weapon.name, s.weapon.cost, s.weapon.element, s.weapon.damage, s.weapon.weaponskill, s.weapon.critical, s.userid))
            #armor
            if c.execute("SELECT playerID FROM armor WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO armor (playerID, name, cost, element, maxhealth, healthregen, money) VALUES ({}, \"{}\", {}, {}, {}, {}, {})".format(s.userid, s.armor.name, s.armor.cost, s.armor.element, s.armor.maxhealth, s.armor.healthregen, s.armor.money))
            else :
                c.execute("UPDATE armor SET name = \"{}\", cost={}, element={}, maxhealth={}, healthregen={}, money={} WHERE playerID = {}".format(s.armor.name, s.armor.cost, s.armor.element, s.armor.maxhealth, s.armor.healthregen, s.armor.money, s.userid))
            conn.commit()    
    except pymysql.err.InternalError as e:
        print(e)
    except pymysql.err.IntegrityError as e:
        print(e)
    finally:
        conn.close()

def getTopPlayers(server="all"):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT playerID, exp FROM items ORDER BY exp DESC")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def resetPlayers():
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("DELETE from items") 
    c.execute("DELETE from busy")
    c.execute("DELETE from tierboss")
    c.execute("DELETE from rpgkings")
    c.execute("DELETE from weapon")
    c.execute("DELETE from armor")
    #stats must be the last one
    c.execute("DELETE from stats")   
    conn.commit()
    conn.close()

def setKing(userid, serverid):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    if c.execute("SELECT playerID FROM rpgkings WHERE serverID={}".format(serverid))==0:
        c.execute("INSERT INTO rpgkings (serverID, playerID) VALUES ('{0}', '{1}')".format(serverid, userid))
    else :
        c.execute("UPDATE rpgkings SET playerID = '{1}' WHERE serverID = {0}".format(serverid, userid))
    conn.commit()
    conn.close()

def getKing(serverid):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT playerID FROM rpgkings WHERE serverID={}".format(serverid))
    king = c.fetchone()
    conn.commit()
    conn.close()
    if king is None:
        return None
    return king[0]

def isKing(userid):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    if c.execute("SELECT serverID FROM rpgkings WHERE playerID={}".format(userid))==0:
        conn.commit()
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True

# Pats
def incrementPats(patterid : int, patteeid : int):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "PATS")
    c = conn.cursor()
    c.execute("SELECT patsNbr FROM pats_counters WHERE patterID={} AND patteeID={}".format(patterid, patteeid))
    pats = c.fetchone()
    if pats == None:
        pats = 1
        c.execute("INSERT INTO pats_counters VALUES ('{}', '{}', '{}')".format(patterid, patteeid, pats))
    else:
        pats = pats[0]+1
        c.execute("UPDATE pats_counters SET patsNbr={} WHERE patterID={} AND patteeID={}".format(pats, patterid, patteeid))
    conn.commit()
    conn.close()
    return pats

