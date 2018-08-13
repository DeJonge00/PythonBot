from rpggame import rpgcharacter as rpgc


class RPGPet(rpgc.RPGCharacter):
    def __init__(self, name, health, maxhealth, damage, weaponskill, critical, exp=0):
        self.exp = exp
        super(RPGPet, self).__init__(name, health, maxhealth, damage, weaponskill, critical)
