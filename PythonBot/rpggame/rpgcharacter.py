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
    def __init__(self, name, health, maxhealth, damage, weaponskill, critical, element=rpgc.element_none):
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.damage = damage
        self.weaponskill = weaponskill
        self.critical = critical

    # Add (negative) health, returns true if successful
    def addHealth(self, n : int, death=True, element=rpgc.element_none):
        if self.health > self.maxhealth:
            self.health = max(0, min(self.health, self.health + n))
            return
        self.health = max(0, min(self.maxhealth, self.health + n))

    def getDamage(self, element=rpgc.element_none):
        return self.damage

    def getWeaponskill(self):
        return self.weaponskill

    def __str__(self, **kwargs):
        return "{} ({})".format(self.name, self.health)

class RPGMonster(RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1, element=rpgc.element_none):
        self.element = element
        super(RPGMonster, self).__init__(name, health, health, damage, ws, 0)

    # Add (negative) health, returns true if successful
    def addHealth(self, n : int, death=True, element=rpgc.element_none):
        if (element == (-1*self.element)):
            n = math.floor(n*1.2)
        if (element == self.element):
            n = math.floor(n*0.8)
        super().addHealth(n)

    def getDamage(self, element = rpgc.element_none):
        n = super().getDamage(element=element)
        # Elemental damage
        selfelem = self.element
        if element != rpgc.element_none:
            if (element == (-1*selfelem)):
                n = math.floor(n*1.2)
            if (element == selfelem):
                n = math.floor(n*0.8)
        return n

class RPGPlayer(RPGCharacter):
    def __init__(self, userid : int, username : str, role="Undead", weapon="Training Sword", armor="Training Robes", health=HEALTH, maxhealth=HEALTH, damage=DAMAGE, ws=WEAPONSKILL, element=rpgc.element_none, critical=0):
        self.userid = userid
        self.role = role
        self.exp = 0
        self.levelups = 0
        self.money = 0
        self.weapon = weapon
        self.armor = armor
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = NONE
        self.critical = critical
        self.bosstier = 1
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws, 0, element=element)

    def addHealth(self, n : int, death=True, element=rpgc.element_none):
        a = rpgc.armor.get(self.armor.lower())
        if a != None:
            abso = a.benefit.get("absorption")
            if abso != None:
               n *= abso
            if (element == (-1*a.element)):
                n = math.floor(n*1.2)
            if (element == a.element):
                n = math.floor(n*0.8)
        super().addHealth(n)
        if (self.health <= 0) & death:
            self.exp -= 100*self.getLevel()
            self.exp = max(0, self.exp)
            self.money = math.floor(self.money*0.5)
            self.busytime = 0

    def buyItem(self, item : rpgsi.RPGShopItem, amount = 1):
        if not player.addMoney(-amount * item.cost):
            return False
        x = item.benefit.get("armor")
        if x!=None:
            if x[0]=="+":
                self.health += x[1]
            if x[0]=="-":
                if self.health>self.maxhealth:
                    self.health = max(self.health-x[1], self.maxhealth)
        x = item.benefit.get("health")
        if x!=None:
            if x[0]=="+":
                self.addHealth(x[1])
            if x[0]=="-":
                self.addHealth(-1*x[1])
        x = item.benefit.get("damage")
        if x!=None:
            if x[0]=="+":
                self.damage += x[1]
            if x[0]=="-":
                self.damage = max(0, self.damage-x[1])
        x = item.benefit.get("critical")
        if x!=None:
            if x[0]=="+":
                self.critical += x[1]
            if x[0]=="-":
                self.critical = max(0, self.critical-x[1])
        return True

    def buyArmor(self, item):
        if not self.addMoney(-1 * item.cost):
            return False
        self.armor = item.name
        return True

    def buyWeapon(self, item):
        if not self.addMoney(-1 * item.cost):
            return False
        self.weapon = item.name
        return True

    def addExp(self, n : int):
        lvl = self.getLevel()
        self.exp += n
        if self.getLevel()>lvl:
            self.levelups += 1
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

    def getDamage(self, element=rpgc.element_none):
        n = super().getDamage(element=element)
        # Elemental damage
        selfelem = rpgc.weapons.get(self.weapon.lower()).element
        if element != rpgc.element_none:
            if (element == (-1*selfelem)):
                n = math.floor(n*1.2)
            if (element == selfelem):
                n = math.floor(n*0.8)
        # Weapon mods
        w = rpgc.weapons.get(self.weapon.lower())
        if w != None:
            m = w.effect.get("damage")
            if m == None:
                return n
            if m[0]=="*":
                return int(math.floor(n*m[1]))
            if m[0]=="-":
                return max(0, n - m[1])
            return n + m[1]
        return n

    def getWeaponskill(self):
        m = rpgc.weapons.get(self.weapon.lower()).effect.get("weaponskill")
        n = super().getWeaponskill()
        if m == None:
            return n
        if m[0]=="*":
            return int(math.floor(n*m[1]))
        if m[0]=="-":
            return max(0, n - m[1])
        return n + m[1]

