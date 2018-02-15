class RPGTrainingItem:
    def __init__(self, name : str, time : int):
        self.name = name
        self.time = time

    def __str__(self):
        return "{}, {}min".format(self.name, self.time)