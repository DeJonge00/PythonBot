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


class RPGCharacter:
    def __init__(self, name, health, maxhealth, damage, weaponskill, critical, element=rpgc.element_none):
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.damage = damage
        self.weaponskill = weaponskill
        self.critical = critical

    @staticmethod
    def get_level_by_exp(exp: int):
        return math.floor(math.sqrt(exp) / 25) + 1

    @staticmethod
    def adjust_stats(n, stat, item, amount=1):
        if item:
            m = item.benefit.get(stat)
            if m:
                if m[0] == "*":
                    return int(math.floor(n * (math.pow(m[1], amount))))
                if m[0] == "-":
                    return max(0, n - (amount * m[1]))
                if m[0] == "+":
                    return n + (amount * m[1])
        return n

    @staticmethod
    def elemental_effect(n, a_elem, d_elem):
        if a_elem != rpgc.element_none:
            if a_elem == (-1 * d_elem):
                n = math.floor(n * 1.2)
            if a_elem == d_elem:
                n = math.floor(n * 0.8)
        return n

    # Add (negative) health, returns true if successful
    def add_health(self, n: int, death=True, element=rpgc.element_none):
        self.health = int(max(0, min(self.get_maxhealth(), self.health + n)))

    def get_maxhealth(self):
        return self.maxhealth

    def get_damage(self, element=rpgc.element_none):
        return self.damage

    def get_critical(self):
        return int(self.critical)

    def get_weaponskill(self):
        return int(self.weaponskill)

    def get_element(self):
        return rpgc.element_none

    def __str__(self, **kwargs):
        return "{} ({})".format(self.name, self.health)






