import discord, math
from discord.ext import commands
from discord.ext.commands import Bot
from rpggame import rpgconstants as rpgc, rpgshopitem as rpgsi, rpgweapon as rpgw, rpgarmor as rpga

# Busydescription status
NONE = 0
ADVENTURE = 1
TRAINING = 2
BOSSRAID = 3
WANDERING = 4

# Min and max busy time
minadvtime = 5
maxadvtime = 120
mintrainingtime = 10
maxtrainingtime = 60
minwandertime = 30
maxwandertime = 360

# Player starting stats
HEALTH = 100
ARMOR = 0
DAMAGE = 10
WEAPONSKILL = 1

def getLevelByExp(exp : int):
    return math.floor(math.sqrt(exp) / 25)+1

def adjustStats(n, stat, item, amount=1):
    if item != None:
        m = item.benefit.get(stat)
        if m != None:
            if m[0]=="*":
                return int(math.floor(n*(math.pow(m[1], amount))))
            if m[0]=="-":
                return max(0, n - (amount*m[1]))
            if m[0]=="+":
                return n + (amount*m[1])
    return n

def elementalEffect(n, a_elem, d_elem):
    if a_elem != rpgc.element_none:
        if (a_elem == (-1*d_elem)):
            n = math.floor(n*1.2)
        if (a_elem == d_elem):
            n = math.floor(n*0.8)
    return n

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
        self.health = int(max(0, min(self.getMaxhealth(), self.health + n)))

    def getMaxhealth(self):
        return self.maxhealth

    def getDamage(self, element=rpgc.element_none):
        return self.damage

    def getCritical(self):
        return int(self.critical)

    def getWeaponskill(self):
        return int(self.weaponskill)

    def __str__(self, **kwargs):
        return "{} ({})".format(self.name, self.health)

    def getElement(self):
        return rpgc.element_none

class RPGMonster(RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1, element=rpgc.element_none):
        self.element = element
        super(RPGMonster, self).__init__(name, health, health, damage, ws, 0)

    def getElement(self):
        return self.element

    def getDamage(self, element = rpgc.element_none):
        n = super().getDamage(element=element)
        return int(elementalEffect(n, self.element, element))
        
class RPGPlayer(RPGCharacter):
    def __init__(self, userid : int, username : str, role="Undead", weapon=rpgw.defaultweapon, armor=rpga.defaultarmor, health=HEALTH, maxhealth=HEALTH, damage=DAMAGE, ws=WEAPONSKILL, critical=0, element=rpgc.element_none):
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
        self.bosstier = 1
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws, critical, element=element)

    def resolveDeath(self):
        if (self.health <= 0):
            self.exp = max(0, self.exp -100*self.getLevel())
            self.money = int(math.floor(self.money*0.5))
            self.busytime = 0

    def addExp(self, n : int):
        if self.health <= 0:
            return
        lvl = self.getLevel()
        self.addMoney(n)
        self.exp += n
        if self.getLevel()>lvl:
            self.levelups += 1

    def addHealth(self, n : int, death=True, element=rpgc.element_none):
        super().addHealth(n)
        if death:
            self.resolveDeath()

    def addMoney(self, n : int):
        if n < 0:
            return False
        n = (1+(self.armor.money/100))*n
        self.money += n

    def subtractMoney(self, n : int):
        if n < 0:
            return False
        if self.money - n < 0:
            return False
        self.money = int(math.floor(self.money - n))
        return True

    def getMaxhealth(self):
        return self.maxhealth + self.armor.maxhealth

    def getElement(self):
        a = self.armor.element
        if a==None:
            return rpgc.element_none
        return a

    def buyItem(self, item : rpgsi.RPGShopItem, amount=1):
        if not self.subtractMoney(amount * item.cost):
            return False
        self.health = min(self.getMaxhealth(), adjustStats(self.health, "health", item, amount=amount))
        self.maxhealth = adjustStats(self.maxhealth, "maxhealth", item, amount=amount)
        self.damage = adjustStats(self.damage, "damage", item, amount=amount)
        self.critical = adjustStats(self.critical, "critical", item, amount=amount)
        return True

    def buyTraining(self, item : rpgsi.RPGShopItem, amount=1):
        self.setMaxhealth(adjustStats(self.maxhealth, "maxhealth", item, amount=amount))
        self.weaponskill = adjustStats(self.weaponskill, "weaponskill", item, amount=amount)

    def buyArmor(self, item : rpga.RPGArmor):
        if not self.subtractMoney(item.cost):
            return False
        self.money += int(math.floor(self.armor.cost*0.25))
        self.armor = item
        self.addHealth(0)
        return True

    def buyWeapon(self, item : rpgw.RPGWeapon):
        if not self.subtractMoney(item.cost):
            return False
        self.money += int(math.floor(self.weapon.cost*0.25))
        self.weapon = item
        return True

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
        if action == WANDERING:
            if not(minwandertime <= time <= maxwandertime):
                return False

        self.busytime = time
        self.busychannel = channel
        self.busydescription = action
        return True

    def resetBusy(self):
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = NONE

    def setMaxhealth(self, n : int):
        r = self.health/self.getMaxhealth()
        self.maxhealth = n
        self.health = int(math.ceil(r*self.getMaxhealth()))

    def getDamage(self, element=rpgc.element_none):
        n = super().getDamage(element=element)
        n = elementalEffect(n, self.weapon.element, element)
        return int(n + self.weapon.damage)

    def getWeaponskill(self):
        n = super().getWeaponskill()
        return int(n + self.weapon.weaponskill)

    def getCritical(self):
        n = super().getCritical()
        return int(n + self.weapon.critical)

    def autoHealthRegen(self):
        self.addHealth((self.getMaxhealth()*0.05)+self.armor.healthregen)