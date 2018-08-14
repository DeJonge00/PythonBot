from rpggame import rpgcharacter as rpgc


class RPGPet(rpgc.RPGCharacter):
    def __init__(self, petid=None, name='Kittycat', health=1, maxhealth=1, damage=1, weaponskill=1, critical=0, exp=0):
        self.petid = petid
        self.exp = exp
        super(RPGPet, self).__init__(name, health, maxhealth, damage, weaponskill, critical)
