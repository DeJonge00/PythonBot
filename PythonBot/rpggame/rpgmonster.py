from rpggame import rpgcharacter as rpgc
from rpggame.rpgplayer import element_none


class RPGMonster(rpgc.RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1, element=element_none):
        self.element = element
        super(RPGMonster, self).__init__(name, health, health, damage, ws, 0)

    def get_element(self):
        return self.element

    def get_damage(self, element=element_none):
        n = super().get_damage(element=element)
        return int(rpgc.RPGCharacter.elemental_effect(n, self.element, element))
