import discord, math
from discord.ext import commands
from discord.ext.commands import Bot

minadvtime = 5
maxadvtime = 120
mintrainingtime = 10
maxtrainingtime = 60

HEALTH = 100
ARMOR = 0
DAMAGE = 10
WEAPONSKILL = 1

def getLevelByExp(exp : int):
    return math.floor(math.sqrt(exp) / 20)+1

class RPGCharacter:
    def __init__(self, name, health, maxhealth, damage, weaponskill):
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.damage = damage
        self.weaponskill = weaponskill
        
    # Add (negative) health, returns true if successful
    def addHealth(self, n : int):
        self.health = max(0, min(self.maxhealth, self.health + n))
        return True

class RPGMonster(RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1):
        super(RPGMonster, self).__init__(name, health, health, damage, ws)

class RPGPlayer(RPGCharacter):
    NONE = 0
    ADVENTURE = 1
    TRAINING = 2

    def __init__(self, userid : int, username : str, role="Undead", health=HEALTH, maxhealth=HEALTH, damage=DAMAGE, ws=WEAPONSKILL):
        self.userid = userid
        self.role = role
        self.exp = 0
        self.money = 0
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = self.NONE
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws)

    def addExp(self, n : int):
        if n<0:
            print("Warning: Exp add below zero (" + str(n) + ") on " + self.user.name)
            return False
        self.exp += n
        self.money += n

    def getLevel(self):
        return getLevelByExp(self.exp)

    def setBusy(self, action : int, time : int, channel : int):
        if self.busytime > 0:
            return False
        if action == self.ADVENTURE:
            if not(minadvtime < time < maxadvtime):
                return False
        if action == self.TRAINING:
            if not(mintrainingtime < time < maxtrainingtime):
                return False

        self.busytime = time
        self.busychannel = channel
        self.busydescription = action
        return True

    def resetBusy(self):
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = self.NONE

    def setAdventure(self, n : int, channelid : int):
        if (self.adventuretime <= 0) & (minadvtime < n < maxadvtime):
            self.adventuretime = n
            self.adventurechannel = channelid

    def addMoney(self, n : int):
        if self.money + n < 0:
            return False
        self.money += n
        return True

    def raiseMaxhealth(self, n : int):
        r = self.health/self.maxhealth
        self.maxhealth += n
        self.health = int(ceil(r*n))