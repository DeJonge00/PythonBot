import asyncio, discord, constants, log, pickle, removeMessage, rpggame.rpgcharacter as rpgchar, pymysql
from discord.ext import commands

# Channels
def initChannels():
    conn = pymysql.connect("localhost", "root", "biribiri", "RPGDB")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS rpgchannel")
    c.execute("CREATE TABLE rpgchannel (serverID INTEGER, channelID INTEGER)")
    conn.commit()
    conn.close()

def setChannel(serverID, channelID):
    conn = pymysql.connect("localhost", "root", "biribiri", "RPGDB")
    c = conn.cursor()
    if c.execute("SELECT * FROM rpgchannel") == 0:
        c.execute("INSERT INTO rpgchannel (serverID, channelID) VALUES ({0}, {1})".format(serverID, channelID))
    else :
        c.execute("UPDATE rpgchannel SET channelID = {0} WHERE serverID = {1}".format(serverID, channelID))
    t = c.fetchone()
    conn.commit()
    conn.close()

# Stats
def initDB():
    conn = pymysql.connect("localhost", "root", "biribiri", "RPGDB")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS stats")
    c.execute("DROP TABLE IF EXISTS items")
    c.execute("DROP TABLE IF EXISTS adventure")
    c.execute("DROP TABLE IF EXISTS weapon")
    c.execute("CREATE TABLE stats (playerID INTEGER PRIMARY KEY, role TEXT, health INTEGER, maxhealth INTEGER, damage INTEGER, weaponskill INTEGER)")
    c.execute("CREATE TABLE items (playerID INTEGER PRIMARY KEY, exp INTEGER, money INTEGER)")
    c.execute("CREATE TABLE adventure (playerID INTEGER PRIMARY KEY, time INTEGER, channelID INTEGER)")
    c.execute("CREATE TABLE weapon (playerID INTEGER PRIMARY KEY, ability TEXT)")
    conn.commit()
    conn.close()

def getPlayer(player : discord.User):
    conn = pymysql.connect("localhost", "root", "biribiri", "RPGDB")
    c = conn.cursor()
    c.execute("SELECT * FROM stats WHERE playerID={}".format(player.id))
    p = c.fetchone()
    c.execute("SELECT * FROM items WHERE playerID={}".format(player.id))
    i = c.fetchone()
    c.execute("SELECT * FROM adventure WHERE playerID={}".format(player.id))
    a = c.fetchone()
    conn.commit()
    conn.close()
    if p == None:
        print("User not found: {}".format(player.name))
        return rpgchar.RPGPlayer(player.id, player.name)
    player = rpgchar.RPGPlayer(player.id, player.name, role=p[1], health=p[2], maxhealth=p[3], damage=p[4], ws=p[5])
    if i != None:
        player.exp = i[1]
        player.money = i[2]
    if a != None:
        player.setAdventure(a[1], a[2])
    return player

def updatePlayers(stats : [rpgchar.RPGPlayer]):
    conn = pymysql.connect("localhost", "root", "biribiri", "RPGDB")
    c = conn.cursor()
    for s in stats:
        if c.execute("SELECT playerID FROM stats WHERE playerID = {0}".format(s.userid)) == 0 :
            c.execute("INSERT INTO stats (playerID, role, health, maxhealth, damage, weaponskill) VALUES ({0}, '{1}', {2}, {3}, {4}, {5})".format(s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill))
        else :
            c.execute("UPDATE stats SET role = '{1}', health = {2} , maxhealth = {3}, damage = {4}, weaponskill = {5} WHERE playerID = {0}".format(s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill))
        
        if c.execute("SELECT playerID FROM items WHERE playerID = {0}".format(s.userid)) == 0 :
            c.execute("INSERT INTO items (playerID, exp, money) VALUES ({0}, {1}, {2})".format(s.playerID, s.exp, s.money))
        else :
            c.execute("UPDATE items SET exp = {1}, money = {2} WHERE playerID = {0}".format(s.playerID, s.exp, s.money))
        
        if c.execute("SELECT playerID FROM adventure WHERE playerID = {0}".format(s.userid)) == 0 :
            c.execute("INSERT INTO adventure (playerID, adventuretime, adventurechannel) VALUES ({0}, {1}, '{2}')".format(s.userid, s.adventuretime, s.adventurechannel))
        else :
            c.execute("UPDATE adventure SET adventuretime = {1}, adventurechannel = '{2}' WHERE playerID = {0}".format(s.userid, s.adventuretime, s.adventurechannel))    
    conn.commit()
    conn.close()

def getTopPlayers(server="all"):
    conn = pymysql.connect("localhost", "root", "biribiri", "RPGDB")
    c = conn.cursor()
    c.execute("SELECT playerID, exp FROM items ORDER BY exp DESC")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a

def getRPGChannel(serverid : str):
    conn = pymysql.connect("localhost", "root", "biribiri", "RPGDB")
    c = conn.cursor()
    c.execute("SELECT channelID FROM rpgchannel WHERE serverID={}".format(serverid))
    t = c.fetchone()
    conn.commit()
    conn.close()
    if t==None:
        print("Channel not specified for server")
        return None
    return self.bot.get_channel(str(t[0]))