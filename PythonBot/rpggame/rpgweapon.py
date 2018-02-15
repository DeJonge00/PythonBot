class RPGWeapon:
    def __init__(self, name : str, cost : int, effect : {str : float}):
        self.name = name
        self.cost = cost
        self.effect = effect

    def __str__(self):
        return "{}, ${} : {}".format(self.name, self.cost, self.effect)