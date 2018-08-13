from rpggame import rpgcharacter as rpgc


class RPGMonster(rpgc.RPGCharacter):
    def __init__(self, name="Monster", health=30, damage=10, ws=1, element=rpgc.element_none):
        self.element = element
        super(RPGMonster, self).__init__(name, health, health, damage, ws, 0)

    def get_element(self):
        return self.element

    def get_damage(self, element=rpgc.element_none):
        n = super().get_damage(element=element)
        return int(rpgc.RPGCharacter.elementalEffect(n, self.element, element))
