from rpggame.rpgcharacter import RPGCharacter
from rpggame.rpgconstants import element_none


class RPGMonster(RPGCharacter):
    def __init__(self, name="Monster", picture_url='https://geekandsundry.com/wp-content/uploads/2016/01/beholder.jpg',
                 health=30, damage=10, ws=1, element=element_none, level=1):
        self.element = element
        self.level = level
        super(RPGMonster, self).__init__(name, picture_url, health, health, damage, ws, 0)

    def get_level(self):
        return self.level

    def get_element(self):
        return self.element

    def get_damage(self, element=element_none):
        n = super().get_damage(element=element)
        return int(RPGCharacter.elemental_effect(n, self.element, element))
