import discord, math
from discord.ext import commands
from discord.ext.commands import Bot

HEALTH = 100
ARMOR = 0
DAMAGE = 10
WEAPONSKILL = 1

def getLevelByExp(exp):
    return math.floor(math.sqrt(exp) / 20)+1

class RPGCharacter:
    def __init__(self, name, health, maxhealth, damage, weaponskill):
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.damage = damage
        self.weaponskill = weaponskill
        
    # Add (negative) health, returns true if successful
    def addHealth(self, n):
        if self.health + n < 0:
            self.health = 0
            return True
        if self.health + n > self.maxhealth:
            self.health = self.maxhealth
            return True
        self.health += n
        return True

class RPGMonster(RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1):
        super(RPGMonster, self).__init__(name, health, health, damage, ws)

class RPGPlayer(RPGCharacter):
    def __init__(self, userid : int, username : str, role="Undead", health=HEALTH, maxhealth=HEALTH, damage=DAMAGE, ws=WEAPONSKILL):
        self.userid = userid
        self.role = role
        self.exp = 0
        self.money = 0
        self.adventuretime = 0
        self.adventurechannel = 0
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws)

    def addExp(self, n):
        if n<0:
            print("Warning: Exp add below zero (" + str(n) + ") on " + self.user.name)
            return False
        self.exp += n
        self.money += n

    def getLevel(self):
        return getLevelByExp(self.exp)

    def setAdventure(self, n : int, channelid : int):
        if (self.adventuretime <= 0) & (5 < n < 120):
            self.adventuretime = n
            self.adventurechannel = channelid

    def addMoney(self, n):
        if money + n < 0:
            return False
        self.money += n
        return True