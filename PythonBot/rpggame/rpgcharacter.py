import discord, math
from discord.ext import commands
from discord.ext.commands import Bot
from rpggame import rpgconstants as rpgc

# Busydescription status
NONE = 0
ADVENTURE = 1
TRAINING = 2
BOSSRAID = 3

# Min and max busy time
minadvtime = 5
maxadvtime = 120
mintrainingtime = 10
maxtrainingtime = 60

# Player starting stats
HEALTH = 100
ARMOR = 0
DAMAGE = 10
WEAPONSKILL = 1

def getLevelByExp(exp : int):
    return math.floor(math.sqrt(exp) / 20)+1

class RPGCharacter:
    def __init__(self, name, health, maxhealth, damage, weaponskill, element=rpgc.element_none):
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.damage = damage
        self.weaponskill = weaponskill
        self.element = element

    # Add (negative) health, returns true if successful
    def addHealth(self, n : int, death=True, element=rpgc.element_none):
        if (element == (-1*self.element)):
            n = math.floor(n*1.2)
        if (element == self.element):
            n = math.floor(n*0.8)
        self.health = max(0, min(self.maxhealth, self.health + n))

    def getDamage(self):
        return self.damage
    def getWeaponskill(self):
        return self.weaponskill

    def __str__(self, **kwargs):
        return "{} ({})".format(self.name, self.health)

class RPGMonster(RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1, element=rpgc.element_none):
        super(RPGMonster, self).__init__(name, health, health, damage, ws, element=element)

class RPGPlayer(RPGCharacter):
    def __init__(self, userid : int, username : str, role="Undead", weapon="Training Sword", health=HEALTH, maxhealth=HEALTH, damage=DAMAGE, ws=WEAPONSKILL, element=rpgc.element_none):
        self.userid = userid
        self.role = role
        self.exp = 0
        self.money = 0
        self.weapon = weapon
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = NONE
        self.bosstier = 1
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws, element=element)

    def addHealth(self, n : int, death=True, element=rpgc.element_none):
        super().addHealth(n, element=element)
        if (self.health <= 0) & death:
            self.exp -= 100*self.getLevel()
            self.money = math.floor(self.money*0.5)
            self.busytime = 0

    def addExp(self, n : int):
        if n<0:
            print("Warning: Exp add below zero (" + str(n) + ") on " + self.user.name)
            return False
        self.exp += n
        self.money += n

    def getLevel(self):
        return getLevelByExp(self.exp)

    def getBosstier(self):
        return self.bosstier

    def addBosstier(self):
        self.bosstier += 1

    def setBusy(self, action : int, time : int, channel : int):
        if self.busytime > 0:
            return False
        if action == ADVENTURE:
            if not(minadvtime <= time <= maxadvtime):
                return False
        if action == TRAINING:
            if not(mintrainingtime <= time <= maxtrainingtime):
                return False

        self.busytime = time
        self.busychannel = channel
        self.busydescription = action
        return True

    def resetBusy(self):
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = NONE

    def setAdventure(self, n : int, channelid : int):
        if (self.busytime <= 0) & (minadvtime < n < maxadvtime):
            self.busytime = n
            self.busychannel = channelid
            self.busydescription = ADVENTURE

    def addMoney(self, n : int):
        if self.money + n < 0:
            return False
        self.money += n
        return True

    def raiseMaxhealth(self, n : int):
        r = self.health/self.maxhealth
        self.maxhealth += n
        self.health = int(math.ceil(r*self.maxhealth))

    def addArmor(self, n : int):
        self.health = max(self.health, self.health + n)

    def getDamage(self):
        m = rpgc.weapons.get(self.weapon.lower()).effect.get("damage")
        if m == None:
            return self.damage
        if m[0]=="*":
            return int(math.floor(self.damage*m[1]))
        if m[0]=="-":
            return self.damage - m[1]
        return self.damage + m[1]

    def getWeaponskill(self):
        m = rpgc.weapons.get(self.weapon.lower()).effect.get("weaponskill")
        if m == None:
            return self.weaponskill
        if m[0]=="*":
            return int(math.floor(self.weaponskill*m[1]))
        if m[0]=="-":
            return self.weaponskill - m[1]
        return self.weaponskill + m[1]
