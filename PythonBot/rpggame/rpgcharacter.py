import math

from rpggame import rpgconstants as rpgc

# Busydescription status
BUSY_DESC_NONE = 0
BUSY_DESC_ADVENTURE = 1
BUSY_DESC_TRAINING = 2
BUSY_DESC_BOSSRAID = 3
BUSY_DESC_WANDERING = 4
BUSY_DESC_WORKING = 5

# Min and max busy time
minadvtime = 5
maxadvtime = 120
mintrainingtime = 10
maxtrainingtime = 60
minwandertime = 30
maxwandertime = 360
minworkingtime = 30
maxworkingtime = 120

# Player starting stats
DEFAULT_HEALTH = 100
DEFAULT_ARMOR = 0
DEFAULT_DAMAGE = 10
DEFAULT_WEAPONSKILL = 1


class RPGCharacter:
    def __init__(self, name, health, maxhealth, damage, weaponskill, critical, element=rpgc.element_none):
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.damage = damage
        self.weaponskill = weaponskill
        self.critical = critical

    def get_level(self):
        return 1

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

    def get_health(self):
        if self.health > self.get_max_health():
            self.health = self.get_max_health()
        return self.health

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
        self.health = int(max(0, min(self.get_max_health(), self.health + n)))

    def get_max_health(self):
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
        return "{} ({}/{})".format(self.name, self.health, self.maxhealth)
