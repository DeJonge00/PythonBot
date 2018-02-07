import asyncio, discord, constants, log, pickle, removeMessage, rpggame.rpgcharacter as rpgchar, sqlite3
from discord.ext import commands

# Channels
def initChannels():
    conn = sqlite3.connect(constants.RPGDB)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS rpgchannel")
    c.execute("CREATE TABLE rpgchannel (serverID INTEGER, channelID INTEGER)")
    conn.commit()
    conn.close()

def setChannel(serverID, channelID):
    conn = sqlite3.connect(constants.RPGDB)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO rpgchannel VALUES (" + str(serverID) + ", " + str(channelID) + ")")
    t = c.fetchone()
    conn.commit()
    conn.close()

# Stats
def initDB():
    conn = sqlite3.connect(constants.RPGDB)
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
    conn = sqlite3.connect(constants.RPGDB)
    c = conn.cursor()
    c.execute("SELECT * FROM stats WHERE playerID=" + str(player.id))
    p = c.fetchone()
    c.execute("SELECT * FROM items WHERE playerID=" + str(player.id))
    i = c.fetchone()
    c.execute("SELECT * FROM adventure WHERE playerID=" + str(player.id))
    a = c.fetchone()
    conn.commit()
    conn.close()
    if p == None:
        print("User not found: " + player.name)
        return rpgchar.RPGPlayer(player.id, player.name)
    player = rpgchar.RPGPlayer(player.id, player.name, role=p[1], health=p[2], maxhealth=p[3], damage=p[4], ws=p[5])
    if i != None:
        player.exp = i[1]
        player.money = i[2]
    if a != None:
        player.setAdventure(i[1], i[2])
    return player

def updatePlayers(stats : [rpgchar.RPGPlayer]):
    conn = sqlite3.connect(constants.RPGDB)
    c = conn.cursor()
    for s in stats:
        params = (s.userid, s.role, s.health, s.maxhealth, s.damage, s.weaponskill)
        c.execute("INSERT OR REPLACE INTO stats VALUES (?, ?, ?, ?, ?, ?)", params)
        params = (s.userid, s.exp, s.money)
        c.execute("INSERT OR REPLACE INTO items VALUES (?, ?, ?)", params)
        params = (s.userid, s.adventuretime, s.adventurechannel)
        c.execute("INSERT OR REPLACE INTO adventure VALUES (?, ?, ?)", params)
    conn.commit()
    conn.close()

def getTopPlayers(server="all"):
    conn = sqlite3.connect(constants.RPGDB)
    c = conn.cursor()
    c.execute("SELECT playerID, exp FROM items ORDER BY exp DESC")
    a = c.fetchall()
    conn.commit()
    conn.close()
    return a
