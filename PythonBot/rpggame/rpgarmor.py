class RPGArmor:
    def __init__(self, name : str, cost : int, absorption : float, element):
        self.name = name
        self.cost = cost
        self.absorption = absorption
        self.element = element

    def __str__(self):
        return "{}, ${} : damage*{} ({})".format(self.name, self.cost, self.effect, self.element)