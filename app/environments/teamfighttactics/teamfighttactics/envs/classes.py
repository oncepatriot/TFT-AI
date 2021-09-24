import random


class Player():
    def __init__(self, id):
        self.id = id
        self.gold = 0
        self.shop = []
        self.bench = []
        self.health = 100
        self.ready = False

class Champion():
    def __init__(self, id, name, level, cost):
        self.id = id
        self.name = name
        self.level = level
        self.cost = cost

class Gragas(Champion):
    def __init__(self, id, name, level, cost):
        super(Gragas, self).__init__(id, name, level)
        self.traits = ["DAWNBRINGER", "BRAWLER"]
        self.cost = 1

class Khaziks(Champion):
    def __init__(self, id, name, level, cost):
        super(Gragas, self).__init__(id, name, level)
        self.cost = 1
        self.traits = ["DAWNBRINGER", "ASSASSIN"]

class Poppy(Champion):
    def __init__(self, id, name, level, cost):
        super(Gragas, self).__init__(id, name, level)
        self.traits = ["HELLION", "KNIGHT"]
        self.cost = 1

class Kled(Champion):
    def __init__(self, id, name, level, cost):
        super(Gragas, self).__init__(id, name, level)
        self.traits = ["HELLION", "CAVALIER"]
        self.cost = 1

class Ziggs(Champion):
    def __init__(self, id, name, level, cost):
        super(Gragas, self).__init__(id, name, level)
        self.traits = ["HELLION", "SPELLWEAVER"]
        self.cost = 1

class Udyr(Champion):
    def __init__(self, id, name, level, cost):
        super(Gragas, self).__init__(id, name, level)
        self.traits = ["DRACONIC", "SKIRMISHER"]
        self.cost = 1

class Olaf(Champion):
    def __init__(self, id, name, level, cost):
        super(Gragas, self).__init__(id, name, level)
        self.traits = ["SENTINEL", "SKIRMISHER"]
        self.cost = 1
