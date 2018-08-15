from discord.ext.commands.errors import CommandInvokeError
import pymysql
from rpggame import rpgweapon as rpgw, rpgarmor as rpga
from rpggame.rpgplayer import RPGPlayer, DEFAULT_ROLE
from rpggame.rpgpet import RPGPet
from secret import secrets


# Channels
def set_rpg_channel(server_id: int, channel_id: str):
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


def get_rpg_channel(server_id: str):
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
def get_busy_players():
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "rpg")
    c = conn.cursor()
    c.execute("SELECT playerid FROM busy WHERE time>0")
    t = c.fetchall()
    conn.commit()
    conn.close()
    players = {}
    for p in t:
        players[p[0]] = get_single_player(p[0])
    return players


TYPE_WEAPON = 0
TYPE_ARMOR = 1
TYPE_PET = 2


def get_single_player(player_id: str):
    playerweapon = None
    playerarmor = None
    playerpets = []

    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "rpg", charset="utf8",
                           use_unicode=True)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM characters WHERE characterid=%s", (player_id,))
        _, exp, health, maxhealth, damage, weaponskill, critical = c.fetchone()
        c.execute("SELECT * FROM players WHERE playerid=%s", (player_id,))
        _, money, role, levelups, bosstier = c.fetchone()
        c.execute("SELECT * FROM items WHERE playerid=%s", (player_id,))
        for _, itemid, type, name in c.fetchall():
            if type in [TYPE_WEAPON, TYPE_ARMOR]:
                c.execute("SELECT * from equipment WHERE equipmentid=%s", (itemid,))
                if type == TYPE_WEAPON:
                    _, cost, element, dam, ws, cr = c.fetchone()
                    playerweapon = rpgw.RPGWeapon(weaponid=itemid, name=name, cost=cost, element=element, damage=dam, weaponskill=ws,
                                                  critical=cr)
                if type == TYPE_ARMOR:
                    _, cost, element, mh, hr, bonusmoney = c.fetchone()
                    playerarmor = rpga.RPGArmor(armorid=itemid, name=name, cost=cost, element=element, maxhealth=mh,
                                                healthregen=hr, money=bonusmoney)
            # if type == TYPE_PET:
            #     c.execute("SELECT * FROM characters WHERE characterid=%s", (itemid,))
            #     _, petexp, hp, mh, dam, ws, cr = c.fetchone()
            #     playerpets.append(
            #         RPGPet(petid=itemid, name=name, exp=petexp, health=hp, maxhealth=mh, damage=dam, weaponskill=ws,
            #                critical=cr))
        c.execute("SELECT * FROM busy WHERE playerid=%s", (player_id,))
        _, desc, time, channel, kingtime = c.fetchone()
    except CommandInvokeError:
        return RPGPlayer(player_id, player_id)
    except TypeError:
        return RPGPlayer(player_id, player_id)
    finally:
        conn.commit()
        conn.close()

    player = RPGPlayer(player_id, str(player_id), role=role, health=health, maxhealth=maxhealth, damage=damage,
                       ws=weaponskill, critical=critical, exp=exp, levelups=levelups, money=money, bosstier=bosstier,
                       kingtimer=kingtime)
    player.set_busy(desc, time, channel)

    if playerweapon:
        player.weapon = playerweapon
    if playerarmor:
        player.armor = playerarmor
    if playerpets:
        player.pets = playerpets
    return player


def update_players(stats: [RPGPlayer]):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "rpg", charset="utf8",
                           use_unicode=True)
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

                if c.execute("SELECT playerid FROM players WHERE playerid = %s", s.userid) == 0:
                    c.execute(
                        "INSERT INTO players (playerid, money, role, levelups, bosstier) VALUES (%s, %s, %s, %s, %s)",
                        (s.userid, s.money, s.role, s.levelups, s.bosstier))
                else:
                    c.execute(
                        "UPDATE players SET money = %s, role = %s, levelups = %s, bosstier = %s WHERE playerid = %s",
                        (s.money, s.role, s.levelups, s.bosstier, s.userid))

                if c.execute("SELECT playerid FROM busy WHERE playerid = %s", s.userid) == 0:
                    c.execute(
                        "INSERT INTO busy (playerid, description, time, channel, kingtime) VALUES (%s, %s, %s, %s, %s)",
                        (s.userid, s.busydescription, s.busytime, s.busychannel, s.kingtimer))
                else:
                    c.execute(
                        "UPDATE busy SET description = %s, time = %s, channel = %s, kingtime = %s WHERE playerid = %s",
                        (s.busytime, s.busychannel, s.busydescription, s.kingtimer, s.userid))

                if s.weapon != rpgw.defaultweapon:
                    if not s.weapon.weaponid:
                        try:
                            c.execute("SELECT equipmentid FROM equipment ORDER BY equipmentid DESC")
                            weaponid = c.fetchone()[0] + 1
                        except:
                            weaponid = 0
                        c.execute(
                            "INSERT INTO equipment (equipmentid, cost, element, bonus1, bonus2, bonus3) VALUES (%s, %s, %s, %s, %s, %s)",
                            (weaponid, s.weapon.cost, s.weapon.element, s.weapon.damage, s.weapon.weaponskill,
                             s.weapon.critical))
                        c.execute("INSERT INTO items (playerid, itemid, type, name) VALUES (%s, %s, %s, %s)",
                                  (s.userid, weaponid, TYPE_WEAPON, s.weapon.name))
                if s.armor != rpga.defaultarmor:
                    if not s.armor.armorid:
                        try:
                            c.execute("SELECT equipmentid FROM equipment ORDER BY equipmentid DESC")
                            armorid = c.fetchone()[0] + 1
                        except:
                            armorid = 0
                        c.execute(
                            "INSERT INTO equipment (equipmentid, cost, element, bonus1, bonus2, bonus3) VALUES (%s, %s, %s, %s, %s, %s)",
                            (s.armor.armorid, s.armor.cost, s.armor.element, s.armor.maxhealth, s.armor.healthregen,
                             s.armor.money))
                        c.execute("INSERT INTO items (playerid, itemid, type, name) VALUES (%s, %s, %s, %s)",
                                  (s.userid, armorid, TYPE_ARMOR, s.armor.name))
                # if s.pets:
                #     print(s.pets)
                #     for p in s.pets:
                #         print(p, p.petid)
                #         if not p.petid:
                #             c.execute(
                #                 "SELECT characterid FROM characters WHERE characterid < 1000000000 ORDER BY characterid DESC")
                #             try:
                #                 petid = c.fetchone()[0] + 1
                #             except:
                #                 petid = 0
                #
                #             c.execute(
                #                 "INSERT INTO characters (characterid, exp, health, maxhealth, damage, weaponskill, critical) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                #                 (petid, p.exp, p.health, p.maxhealth, p.damage, p.weaponskill, p.critical))
                #             c.execute("INSERT INTO items (playerid, itemid, type, name) VALUES (%s, %s, %s, %s)",
                #                       (s.userid, petid, TYPE_PET, p.name))
                #         else:
                #             c.execute(
                #                 "UPDATE characters SET exp=%s, health=%s, maxhealth=%s, damage=%s, weaponskill=%s, critical=%s WHERE characterid=%s",
                #                 (p.exp, p.health, p.maxhealth, p.damage, p.weaponskill, p.critical, p.petid))
                #         # TODO Add pet nicknames
                #         # TODO Remove pets without reference

                conn.commit()
    except pymysql.err.InternalError as e:
        print(e)
    except pymysql.err.IntegrityError as e:
        print(e)
    finally:
        conn.close()


def get_top_players(group: str, amount: int):
    conn = pymysql.connect(secrets.DBAddress, secrets.DBName, secrets.DBPassword, "rpg")
    c = conn.cursor()
    try:
        if group in ['money', 'bosstier']:
            c.execute("SELECT playerid, {0} FROM items ORDER BY {0} DESC LIMIT {1}".format(group, amount))
        elif group in ['exp', 'damage', 'weaponskill', 'critical']:
            c.execute("SELECT characterid, {0} FROM characters ORDER BY {0} DESC LIMIT {1}".format(group, amount))
        else:
            return None
        a = c.fetchall()
    finally:
        conn.commit()
        conn.close()
    return a

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
        pats = pats[0] + 1
        c.execute("UPDATE pats_counters SET patsNbr=%s WHERE patterID=%s AND patteeID=%s", (pats, patter_id, pattee_id))
    else:
        pats = 1
        c.execute("INSERT INTO pats_counters VALUES (%s, %s, %s)", (patter_id, pattee_id, pats))
    conn.commit()
    conn.close()
    return pats
