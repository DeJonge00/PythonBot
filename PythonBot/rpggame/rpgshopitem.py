class RPGShopItem:
    def __init__(self, name : str, cost : int, benefit : {str : (str, float)}):
        self.name = name
        self.cost = cost # Minutes or Money
        self.benefit = benefit
    def __str__(self):
        return "{}, ${} : {}".format(self.name, self.cost, self.benefit)

class RPGInvItem(RPGShopItem):
    def __init__(self, name : str, cost : int, benefit : {str : (str, float)}, element):
        self.element = element
        super(RPGInvItem, self).__init__(name, cost, benefit)

    def __str__(self):
        return "{}, ${} : {} ({})".format(self.name, self.cost, self.benefit, self.element)