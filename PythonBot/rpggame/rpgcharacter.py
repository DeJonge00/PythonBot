import discord, math
from discord.ext import commands
from discord.ext.commands import Bot

HEALTH = 100
ARMOR = 0
DAMAGE = 10
WEAPONSKILL = 1

class RPGCharacter:
    def __init__(self, n, health=HEALTH, damage=DAMAGE, weaponskill=WEAPONSKILL):
        self.name = n
        self.health = health
        self.maxhealth = health
        self.damage = damage
        self.weaponskill = weaponskill
        
    # Add (negative) health, returns true if successful
    async def addHealth(self, n):
        if(n<-10000 | n>10000):
            print("AddHealth out of bounds")
            return False
        if self.health + n < 0:
            self.health = 0
            return True
        if self.health + n > self.maxhealth:
            self.health = self.maxhealth
            return True
        self.health += n
        return True

class RPGPlayer(RPGCharacter):
    def __init__(self, user : discord.User, role="Undead"):
        self.user = user
        self.role = role
        self.exp = 0
        self.money = 0
        self.adventure = 0
        super(RPGPlayer, self).__init__(user.name)

    async def addExp(self, n):
        if n<0:
            return print("Warning: Exp add below zero (" + str(n) + ") on " + self.name)
        self.exp += n
        self.money += n

    async def getLevel(self):
        return math.floor(math.sqrt(self.exp) / 20)

    async def setAdventure(self, n):
        if (self.adventure <= 0) & (5 < n < 120):
            self.adventure = n