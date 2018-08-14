class RPGShopItem:
    def __init__(self, name: str, cost: float, benefit: {str: (str, float)}):
        self.name = name
        self.cost = cost  # Minutes or Money
        self.benefit = benefit

    def __str__(self):
        return "{}, ${} : {}".format(self.name, self.cost, self.benefit)
