class RPGShopItem:
    def __init__(self, name : str, cost : int, benefit : {str : (str, float)}):
        self.name = name
        self.cost = cost # Minutes or Money
        self.benefit = benefit

class RPGInvItem(RPGShopItem):
    def __init__(self, name : str, cost : int, effect : {str : (str, float)}, element):
        self.element = element
        super(RPGInvItem, self).__init__(name, cost, effect)

    def __str__(self):
        return "{}, ${} : {} ({})".format(self.name, self.cost, self.effect, self.element)