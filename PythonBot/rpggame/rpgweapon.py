import random, ipdb
from random import randint
from rpggame import rpgconstants as rpgc


def generateWeapon(cost : int):
#    name = "Weapon{}".format(cost)
    name = str(random.choice(rpgc.weaponprefixes)) + " " + str(random.choice(rpgc.weaponelems)) + " " + str(random.choice(rpgc.weapons)) + " " + str(random.choice(rpgc.weaponsuffixes))
    n = randint(0,99)
    damage = weaponskill = critical = 0
    if n<45:
        damage = randint(int(0.005*cost),int(0.015*cost))
    elif n<80:
        weaponskill = randint(int(0.001*cost),int(0.005*cost))
    else:
        critical = randint(int(0.001*cost),int(0.002*cost))
    return RPGWeapon(name, cost, 1, damage, weaponskill, critical)

class RPGWeapon:
    def __init__(self, name : str, cost : int, element=1, damage=0, weaponskill=0, critical=0):
        self.name = name
        self.cost = cost
        self.element = element
        self.damage = damage
        self.weaponskill = weaponskill
        self.critical = critical

    def __str__(self):
        return "{}: d+{}, ws+{}, c+{}".format(self.name, self.damage, self.weaponskill, self.critical)

defaultweapon = RPGWeapon("Training Sword", 0)
