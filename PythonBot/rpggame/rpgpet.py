from rpggame import rpgcharacter as rpgc
import math


class RPGPet(rpgc.RPGCharacter):
    def __init__(self, petid=None, name='Kittycat', health=1, maxhealth=1, damage=1, weaponskill=1, critical=0, exp=0):
        self.petid = petid
        self.exp = exp
        super(RPGPet, self).__init__(name, health, maxhealth, damage, weaponskill, critical)

    def add_exp(self, n: int):
        if self.health <= 0:
            return
        lvl = self.get_level()
        self.exp += n
        lvl = self.get_level() - lvl
        if lvl > 0:
            self.damage += 10 * lvl
            self.weaponskill += lvl

    @staticmethod
    def get_level_by_exp(exp: int):
        return math.floor(math.sqrt(exp) / 15) + 1

    def get_level(self):
        return RPGPet.get_level_by_exp(self.exp)
