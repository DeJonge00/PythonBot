import discord, math
from rpggame import rpgshop
from discord.ext import commands
from discord.ext.commands import Bot

# Busydescription status
NONE = 0
ADVENTURE = 1
TRAINING = 2

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

names = {"role" : ["Undead", "Assassin", "Lancer", "Rider", "Caster", "Archer", "Berserker", "Saber"], 
         "monster" : ["Goblin", "Gretchin", "Elven Slave", "Giant Spider", "Wounded Troll", "Lone Chaos Marauder", "Black Wolf", "Evolved Fish", "Drunk Human"],
         "boss" : ["Black Ork Boss", "Yeti", "Mammoth", "Ogre Bruiser", "Chaos Demon of Khorne", "Chaos Sorcerer", "Unknown Mutation", "Young Dragon"]
         }

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

    def getDamage():
        return self.damage
    def getWeaponskill():
        return self.weaponskill

class RPGMonster(RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1):
        super(RPGMonster, self).__init__(name, health, health, damage, ws)

class RPGPlayer(RPGCharacter):
    def __init__(self, userid : int, username : str, role="Undead", weapon="Training sword", health=HEALTH, maxhealth=HEALTH, damage=DAMAGE, ws=WEAPONSKILL):
        self.userid = userid
        self.role = role
        self.exp = 0
        self.money = 0
        self.weapon = weapon
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = NONE
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws)

    def addHealth(self, n : int):
        super().addHealth(n)
        if self.health <= 0:
            self.exp -= 100*self.getLevel()
            self.money = math.floor(self.money*0.5)

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

    def getDamage():
        m = rpgshop.weapons.get(self.weapon).get("damage")
        if m == None:
            return self.damage()
        if 0 <= m < 2:
            return int(math.floor(self.damage()*m))
        return self.damage() + m

    def getWeaponskill():
        m = rpgshop.weapons.get(self.weapon).get("weaponskill")
        if m == None:
            return self.weaponskill()
        if 0 <= m < 2:
            return int(math.floor(self.weaponskill()*m))
        return self.weaponskill() + m