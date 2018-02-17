class RPGWeapon:
    def __init__(self, name : str, cost : int, effect : {str : (str, float)}, element):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.element = element

    def __str__(self):
        return "{}, ${} : {} ({})".format(self.name, self.cost, self.effect, self.element)