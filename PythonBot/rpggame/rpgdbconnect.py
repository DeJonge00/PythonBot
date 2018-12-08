import discord
import pymysql
from rpggame import rpgweapon as rpgw, rpgarmor as rpga
from rpggame.rpgplayer import RPGPlayer, DEFAULT_ROLE
from rpggame.rpgpet import RPGPet
from secret import secrets
from discord import Client


# Channels
def set_rpg_channel(server_id: int, channel_id: str):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="rpg", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT channelID FROM rpgchannel WHERE serverID=%s", server_id)
    t = c.fetchone()
    if not t:
        c.execute("INSERT INTO rpgchannel VALUES ('{}', '{}')".format(server_id, channel_id))
    else:
        c.execute("UPDATE rpgchannel SET channelID={} WHERE serverID={}".format(channel_id, server_id))
    conn.commit()
    conn.close()


def get_rpg_channel(server_id: str):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="rpg", charset="utf8", use_unicode=True)
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
def get_busy_players(bot: Client):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="rpg", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT playerid FROM busy WHERE time>0")
    t = c.fetchall()
    t = [x[0] for x in t]
    conn.commit()
    conn.close()
    players = {}
    for p in t:
        players[str(p)] = get_single_player(bot, p)
    return players


def get_all_players(bot: Client):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="rpg", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT playerid FROM busy")
    t = c.fetchall()
    conn.commit()
    conn.close()
    players = [get_single_player(bot, p) for p in [x[0] for x in t]]
    return players


TYPE_WEAPON = 0
TYPE_ARMOR = 1
TYPE_PET = 2


def get_single_player(bot: discord.Client, player_id: str):
    player = None
    username = {str(x.id): str(x.name) for x in bot.get_all_members() if str(x.id) == str(player_id)}.get(
        str(player_id), str(player_id))

    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword, database="rpg", charset="utf8", use_unicode=True)
    c = conn.cursor()
    try:
        # Get basic playerinfo
        c.execute("SELECT * FROM characters WHERE characterid=%s", (player_id,))
        _, exp, health, maxhealth, damage, weaponskill, critical = c.fetchone()
        c.execute("SELECT * FROM players WHERE playerid=%s", (player_id,))
        _, money, role, levelups, bosstier, extratime = c.fetchone()
        player = RPGPlayer(userid=player_id, pets=[], username=username, role=role, health=health,
                           maxhealth=maxhealth, damage=damage,
                           ws=weaponskill, critical=critical, exp=exp, levelups=levelups, money=money,
                           bosstier=bosstier, extratime=extratime)

        # Get players current action
        c.execute("SELECT * FROM busy WHERE playerid=%s", (player_id,))
        _, desc, time, channel, kingtime = c.fetchone()
        player.set_busy(desc, time, channel)
        player.kingtimer = kingtime

        # Get players items
        c.execute("SELECT * FROM items WHERE playerid=%s", (player_id,))
        for _, item_id, item_type, name in c.fetchall():
            if item_type in [TYPE_WEAPON, TYPE_ARMOR]:
                c.execute("SELECT * from equipment WHERE equipmentid=%s", (item_id,))
                if item_type == TYPE_WEAPON:
                    weaponid, cost, element, dam, ws, cr = c.fetchone()
                    player.weapon = rpgw.RPGWeapon(weaponid=weaponid, name=name, cost=cost, element=element, damage=dam,
                                                   weaponskill=ws,
                                                   critical=cr)
                if item_type == TYPE_ARMOR:
                    armorid, cost, element, mh, hr, bonusmoney = c.fetchone()
                    player.armor = rpga.RPGArmor(armorid=armorid, name=name, cost=cost, element=element, maxhealth=mh,
                                                 healthregen=hr, money=bonusmoney)
            if item_type == TYPE_PET:
                c.execute("SELECT * FROM characters WHERE characterid=%s", (item_id,))
                petid, petexp, hp, mh, dam, ws, cr = c.fetchone()
                player.add_pet(
                    RPGPet(petid=petid, name=name, exp=petexp, health=hp, maxhealth=mh, damage=dam, weaponskill=ws,
                           critical=cr))
    finally:
        conn.commit()
        conn.close()
        return player if player else RPGPlayer(player_id, player_id)


def update_players(stats: [RPGPlayer]):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="rpg", charset="utf8", use_unicode=True)
    c = conn.cursor()
    try:
        for s in stats:
            if s.role is not DEFAULT_ROLE:
                if c.execute("SELECT characterid FROM characters WHERE characterid = %s", (s.userid,)) == 0:
                    c.execute(
                        "INSERT INTO characters (characterid, exp, health, maxhealth, damage, weaponskill, critical) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (s.userid, s.exp, s.health, s.maxhealth, s.damage, s.weaponskill, s.critical))
                else:
                    c.execute(
                        "UPDATE characters SET exp = %s, health = %s , maxhealth = %s, damage = %s, weaponskill = %s, critical = %s WHERE characterid = %s",
                        (s.exp, s.health, s.maxhealth, s.damage, s.weaponskill, s.critical, s.userid))
                conn.commit()
                if c.execute("SELECT playerid FROM players WHERE playerid = %s", s.userid) == 0:
                    c.execute(
                        "INSERT INTO players (playerid, money, role, levelups, bosstier, extratime) VALUES (%s, %s, %s, %s, %s, %s)",
                        (s.userid, s.money, s.role, s.levelups, s.bosstier, s.extratime))
                else:
                    c.execute(
                        "UPDATE players SET money = %s, role = %s, levelups = %s, bosstier = %s, extratime = %s WHERE playerid = %s",
                        (s.money, s.role, s.levelups, s.bosstier, s.extratime, s.userid))
                conn.commit()
                if c.execute("SELECT playerid FROM busy WHERE playerid = %s", s.userid) == 0:
                    c.execute(
                        "INSERT INTO busy (playerid, description, time, channel, kingtime) VALUES (%s, %s, %s, %s, %s)",
                        (s.userid, s.busydescription, s.busytime, s.busychannel, s.kingtimer))
                else:
                    c.execute(
                        "UPDATE busy SET description = %s, time = %s, channel = %s, kingtime = %s WHERE playerid = %s",
                        (s.busydescription, s.busytime, s.busychannel, s.kingtimer, s.userid))
                conn.commit()
                if s.weapon != rpgw.RPGWeapon():
                    # delete weapons that arent in the RPGPlayers slot
                    c.execute("SELECT itemid FROM items WHERE playerid = %s AND type = %s", (s.userid, TYPE_WEAPON))
                    old_weapons = c.fetchall()
                    for p in old_weapons:
                        if p[0] != s.weapon.weaponid:
                            c.execute("DELETE FROM equipment WHERE equipmentid = %s", (p[0],))
                            c.execute("DELETE FROM items WHERE itemid = %s", (p[0],))

                    if not s.weapon.weaponid:
                        try:
                            c.execute("SELECT equipmentid FROM equipment ORDER BY equipmentid DESC")
                            weaponid = c.fetchone()[0] + 1
                        except:
                            weaponid = 1
                        c.execute(
                            "INSERT INTO equipment (equipmentid, cost, element, bonus1, bonus2, bonus3) VALUES (%s, %s, %s, %s, %s, %s)",
                            (weaponid, s.weapon.cost, s.weapon.element, s.weapon.damage, s.weapon.weaponskill,
                             s.weapon.critical))
                        c.execute("INSERT INTO items (playerid, itemid, type, name) VALUES (%s, %s, %s, %s)",
                                  (s.userid, weaponid, TYPE_WEAPON, s.weapon.name))
                    conn.commit()
                if s.armor != rpga.RPGArmor():
                    # delete armors that arent in the RPGPlayers slot
                    c.execute("SELECT itemid FROM items WHERE playerid = %s AND type = %s", (s.userid, TYPE_ARMOR))
                    old_armor = c.fetchall()
                    for p in old_armor:
                        if p[0] != s.armor.armorid:
                            c.execute("DELETE FROM equipment WHERE equipmentid = %s", (p[0],))
                            c.execute("DELETE FROM items WHERE itemid = %s", (p[0],))
                    if not s.armor.armorid:
                        try:
                            c.execute("SELECT equipmentid FROM equipment ORDER BY equipmentid DESC")
                            armorid = c.fetchone()[0] + 1
                        except:
                            armorid = 1
                        c.execute(
                            "INSERT INTO equipment (equipmentid, cost, element, bonus1, bonus2, bonus3) VALUES (%s, %s, %s, %s, %s, %s)",
                            (armorid, s.armor.cost, s.armor.element, s.armor.maxhealth, s.armor.healthregen,
                             s.armor.money))
                        c.execute("INSERT INTO items (playerid, itemid, type, name) VALUES (%s, %s, %s, %s)",
                                  (s.userid, armorid, TYPE_ARMOR, s.armor.name))
                    conn.commit()
                if s.pets:
                    # delte pets that arent in the RPGPlayers petslist
                    c.execute("SELECT itemid FROM items WHERE playerid = %s AND type > 1", (s.userid,))
                    old_pets = c.fetchall()
                    for p in old_pets:
                        if p[0] not in [x.petid for x in s.pets]:
                            c.execute("DELETE FROM characters WHERE characterid = %s", (p[0],))
                            c.execute("DELETE FROM items WHERE itemid = %s", (p[0],))

                    # Add or update RPGPlayers pets to the database
                    for p in s.pets:
                        if not p.petid:
                            c.execute(
                                "SELECT characterid FROM characters WHERE characterid < 1000000000 ORDER BY characterid DESC")
                            try:
                                petid = c.fetchone()[0] + 1
                            except:
                                petid = 1

                            c.execute(
                                "INSERT INTO characters (characterid, exp, health, maxhealth, damage, weaponskill, critical) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (petid, p.exp, p.health, p.maxhealth, p.damage, p.weaponskill, p.critical))
                            c.execute("INSERT INTO items (playerid, itemid, type, name) VALUES (%s, %s, %s, %s)",
                                      (s.userid, petid, TYPE_PET, p.name))
                        else:
                            c.execute(
                                "UPDATE characters SET exp=%s, health=%s, maxhealth=%s, damage=%s, weaponskill=%s, critical=%s WHERE characterid=%s",
                                (p.exp, p.health, p.maxhealth, p.damage, p.weaponskill, p.critical, p.petid))

                conn.commit()
    except pymysql.err.InternalError as e:
        print(e)
    except pymysql.err.IntegrityError as e:
        print(e)
    finally:
        conn.close()


def get_top_players(bot: discord.Client, group: str, amount: int):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="rpg", charset="utf8", use_unicode=True)
    c = conn.cursor()
    try:
        if group in ['money', 'bosstier']:
            c.execute("SELECT playerid, {0} FROM players ORDER BY {0} DESC LIMIT {1}".format(group, amount))
        else:
            c.execute(
                "SELECT characterid, {0} FROM characters WHERE characterid > 1000000 ORDER BY {0} DESC LIMIT {1}".format(
                    group, amount))
        a = c.fetchall()
        result = []
        for i in range(len(a)):
            try:
                result.append((get_single_player(bot, a[i][0]).name, a[i][1]))
            except:
                result.append(('id' + str(a[i][0]), a[i][1]))

    finally:
        conn.commit()
        conn.close()
    return result


#
# def reset_rpg_database():
#     conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "rpg")
#     c = conn.cursor()
#     c.execute("DELETE from busy")
#     c.execute("DELETE from equipment")
#     c.execute("DELETE from players")
#     c.execute("DELETE from characters")
#     c.execute("DELETE from items")
#     conn.commit()
#     conn.close()


def setKing(user_id, server_id):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="RPGDB", charset="utf8", use_unicode=True)
    c = conn.cursor()
    if c.execute("SELECT playerID FROM rpgkings WHERE serverID=%s", server_id) == 0:
        c.execute("INSERT INTO rpgkings (serverID, playerID) VALUES (%s, %s)", (server_id, user_id))
    else:
        c.execute("UPDATE rpgkings SET playerID = %s WHERE serverID = %s", (user_id, server_id))
    conn.commit()
    conn.close()


def getKing(server_id):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="RPGDB", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT playerID FROM rpgkings WHERE serverID=%s", server_id)
    king = c.fetchone()
    conn.commit()
    conn.close()
    return king[0] if king else None


def isKing(user_id):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="RPGDB", charset="utf8", use_unicode=True)
    c = conn.cursor()
    r = c.execute("SELECT serverID FROM rpgkings WHERE playerID=%s ", user_id)
    conn.commit()
    conn.close()
    return False if r == 0 else True


# Pats
def increment_pats(patter_id: str, pattee_id: str):
    conn = pymysql.connect(host=secrets.DBAddress, port=secrets.DBPort, user=secrets.DBName,
                           password=secrets.DBPassword,
                           database="PATS", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT patsNbr FROM pats_counters WHERE patterID=%s AND patteeID=%s", (patter_id, pattee_id))
    pats = c.fetchone()
    if pats:
        pats = pats[0] + 1
        c.execute("UPDATE pats_counters SET patsNbr=%s WHERE patterID=%s AND patteeID=%s", (pats, patter_id, pattee_id))
    else:
        pats = 1
        c.execute("INSERT INTO pats_counters VALUES (%s, %s, %s)", (patter_id, pattee_id, pats))
    conn.commit()
    conn.close()
    return pats
