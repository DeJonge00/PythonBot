class rpgshopitem:
    def __init__(self, name : str, cost : int):
        self.name = name
        self.cost = cost

    def getName(self):
        return self.name

    def getCost(self):
        return self.cost