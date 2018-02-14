class RPGWeapon:
    def __init__(self, name : str, cost : int, effect : {str : float}):
        self.name = name
        self.cost = cost
        self.effect = effect