import random, math
from random import randint
from rpggame import rpgconstants as rpgc


class RPGArmor:
    def __init__(self, armorid=None, name="Training Robes", cost=0, element=1, maxhealth=0, healthregen=0, money=0):
        self.armorid = armorid
        self.name = name
        self.cost = cost
        self.element = element
        self.maxhealth = maxhealth
        self.healthregen = healthregen
        self.money = money

    def __str__(self):
        return "{}: mh+{}, hr+{}, m+{}%".format(self.name, self.maxhealth, self.healthregen, self.money)

    def as_dict(self):
        return {
            'name': self.name,
            'cost': self.cost,
            'element': self.element,
            'maxhealth': self.maxhealth,
            'healthregen': self.healthregen,
            'money': self.money
        }


def dict_to_armor(weapon: dict):
    return RPGArmor(
        name=weapon.get('name'),
        cost=weapon.get('cost'),
        element=weapon.get('element'),
        maxhealth=weapon.get('maxhealth'),
        healthregen=weapon.get('healthregen'),
        money=weapon.get('money')
    )


def generateArmor(cost: int):
    name = str(random.choice(rpgc.prefixes))
    i = random.choice(list(rpgc.elementnames.keys()))
    name += " " + rpgc.elementnames.get(i)[1] + " " + str(random.choice(rpgc.armors)) + " " + str(
        random.choice(rpgc.suffixes))

    maxhealth = healthregen = money = 0
    points = math.floor(cost / 100)
    first = randint(0, 99)
    if first < 45:
        r = randint(0, points)
        maxhealth += int(r * 1.5)
        points -= r
    elif first < 80:
        r = randint(0, points)
        healthregen += int(r / 5.5)
        points -= r
    else:
        r = randint(0, points)
        money += int(r / 30)
        maxhealth -= int(r)
        points -= r

    second = randint(0, 99)
    if second < 45:
        maxhealth += int(points * 1.5)
    elif second < 80:
        healthregen += int(points / 5.5)
    else:
        money += int(points / 30)
        maxhealth -= int(points)
    return RPGArmor(name=name, cost=cost, element=i, maxhealth=maxhealth, healthregen=healthregen, money=money)
