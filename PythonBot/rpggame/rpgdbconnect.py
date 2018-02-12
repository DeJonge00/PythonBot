import asyncio, discord, constants, log, pickle, removeMessage, rpggame.rpgcharacter as rpgchar, pymysql
from discord.ext import commands
from secret import secrets

# Channels
def initChannels():
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS rpgchannel")
    c.execute("CREATE TABLE rpgchannel (serverID INTEGER, channelID INTEGER)")
    conn.commit()
    conn.close()

def setRPGChannel(serverid : int, channelid : int):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT channelID FROM rpgchannel ".format(serverid))
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
    return self.bot.get_channel(str(t[0]))

# Rpg
def initRpgDB():
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS stats")
    c.execute("DROP TABLE IF EXISTS items")
    c.execute("DROP TABLE IF EXISTS busy")
    c.execute("DROP TABLE IF EXISTS weapon")
    c.execute("CREATE TABLE stats (playerID INTEGER PRIMARY KEY, role TEXT, health INTEGER, maxhealth INTEGER, damage INTEGER, weaponskill INTEGER)")
    c.execute("CREATE TABLE items (playerID INTEGER PRIMARY KEY, exp INTEGER, money INTEGER)")
    c.execute("CREATE TABLE busy (playerID INTEGER PRIMARY KEY, busytime INTEGER, busychannel INTEGER, busydesc INTEGER)")
    c.execute("CREATE TABLE weapon (playerID INTEGER PRIMARY KEY, ability TEXT)")
    conn.commit()
    conn.close()

def getPlayer(player : discord.User):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    c.execute("SELECT * FROM stats WHERE playerID={}".format(player.id))
    p = c.fetchone()
    c.execute("SELECT * FROM items WHERE playerID={}".format(player.id))
    i = c.fetchone()
    c.execute("SELECT * FROM busy WHERE playerID={}".format(player.id))
    a = c.fetchone()
    conn.commit()
    conn.close()
    if p == None:
        try:
            print("User not found: {}".format(player.name))
        except UnicodeEncodeError:
            pass
        return rpgchar.RPGPlayer(player.id, player.name)
    player = rpgchar.RPGPlayer(player.id, player.name, role=p[1], health=p[2], maxhealth=p[3], damage=p[4], ws=p[5])
    if i != None:
        player.exp = i[1]
        player.money = i[2]
    if a != None:
        player.setBusy(a[3], a[1], a[2])
    return player

def updatePlayers(stats : [rpgchar.RPGPlayer]):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "RPGDB")
    c = conn.cursor()
    try:
        for s in stats:
            if c.execute("SELECT playerID FROM stats WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO stats (playerID, role, health, maxhealth, damage, weaponskill) VALUES ({0}, '{1}', {2}, {3}, {4}, {5})".format(s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill))
            else :
                c.execute("UPDATE stats SET role = '{1}', health = {2} , maxhealth = {3}, damage = {4}, weaponskill = {5} WHERE playerID = {0}".format(s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill))
        
            if c.execute("SELECT playerID FROM items WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO items (playerID, exp, money) VALUES ({0}, {1}, {2})".format(s.userid, s.exp, s.money))
            else :
                c.execute("UPDATE items SET exp = {1}, money = {2} WHERE playerID = {0}".format(s.userid, s.exp, s.money))
            if c.execute("SELECT playerID FROM busy WHERE playerID = {0}".format(s.userid)) == 0 :
                c.execute("INSERT INTO busy (playerID, busytime, busychannel, busydescr) VALUES ({0}, {1}, '{2}', '{3}')".format(s.userid, s.busytime, s.busychannel, s.busydescription))
            else :
                c.execute("UPDATE busy SET busytime = {1}, busychannel = '{2}', busydescr='{3}' WHERE playerID = {0}".format(s.userid, s.busytime, s.busychannel, s.busydescription))
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