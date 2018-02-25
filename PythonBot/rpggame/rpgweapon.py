import random, math
from random import randint
from rpggame import rpgconstants as rpgc


def generateWeapon(cost : int):
    name = str(random.choice(rpgc.weaponprefixes))
    i = randint(0, len(rpgc.weaponelems)-1)
    name += " " + rpgc.weaponelems[i] + " " + str(random.choice(rpgc.weapons)) + " " + str(random.choice(rpgc.weaponsuffixes))
    elem = math.ceil((i+2)/2)
    if i%2==0:
        elem *= -1

    damage = weaponskill = critical = 0
    points = math.floor(cost/90)
    first = randint(0, 99)
    if first < 45:
        r = randint(0, points)
        damage += r
        points -= r
    elif first < 80:
        r = randint(0, points)
        weaponskill += math.floor(r/3)
        points -= r
    else:
        r = randint(0, points)
        critical += math.floor(r/7)
        points -= r

    second = randint(0, 99)
    if second < 45:
        damage += points
    elif second < 80:
        weaponskill += math.floor(points/3)
    else:
        critical += math.floor(points/7)
    return RPGWeapon(name, cost, elem, damage, weaponskill, critical)

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
