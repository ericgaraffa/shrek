import numpy as np
import random

MAP_HEIGHT = 16
MAP_WIDTH = 16
MAX_CHILD = 10

directions = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

entities = {
    0: "sol",
    1: "pont",
    2: "arbre",
    3: "rocher",
    4: "eau",
    5: "standard",
    6: "fille",
    7: "garçon",
    8: "chapeau",
    9: "instrument",
    10: "tombe",
    11: "poussière",
    12: "ossement",
    13: "rien",
    14: "shrek"
}

visuel = {
    "sol": " ",
    "pont": "=",
    "arbre": "*",
    "rocher": "r",
    "eau": "o",
    "enfant": "e",
    "shrek": "X",
    "standard": "S",
    "fille": "F",
    "garçon": "G",
    "chapeau": "C",
    "instrument": "I",
    "tombe": "T",
    "poussière": "P",
    "ossement": "?",
    "rien": "R"
}


class Entity:
    def __init__(self, x, y):
        self.visuel = random.choice([0, 1])
        self.x = x
        self.y = y
        self.cross = 0

    def getVisuel(self):
        return self.visuel

    def move(self, carte):
        return

class Child(Entity):
    def __init__(self, x, y):
        self.visuel = random.choice([5, 6, 7, 8, 9])
        self.death = 0

    def move(self, carte):
        h, w = carte.shape()
        for dx, dy in directions.values():
            if 0 <= self.x + dx < h and 0 <= self.y + dy < w and (carte[self.x + dx, self.y + dy] <= 2 or carte[self.x + dx, self.y + dy] > 5 or carte[self.x + dx, self.y + dy] <= 9):  # pas d'obstacle || child
                self.x += dx
                self.y += dy

                # todo mettre à jour la carte

                return carte
        return carte

    def getVisuel(self):
        return self.visuel

    def death(self):
        self.death = 1
        self.visuel = random.choice([10, 11, 12, 13])
        return


class Shrek(Entity):
    def __init__(self, x, y):
        self.visuel = 14

    def eat(self, Child):
        Child.death()
        return

    def getVisuel(self):
        return self.visuel

    def move(self):
        return


class Obastacle(Entity):
    def __init__(self, x, y):
        self.type = random.choice([2, 3, 4])
        self.cross = 1

    def getVisuel(self):
        return self.type


class Map:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.nbChild = 0
        self.nbShrek = 0
        self.obstaclesArray = []
        self.entitysArray = []

    def getObstacles(self):
        return self.obstaclesArray

    def getEntitys(self):
        return self.entitysArray

    def create_random_map(self):
        carte = np.zeros((self.h, self.w), dtype=int)

        # generation des entites
        for i in range(self.h):
            for j in range(self.w):
                if i < 2 or i > self.h - 3 or j < 2 or j > self.w - 3:
                    carte[i, j] = 2
                elif random.random() < 0.3:
                    o = Obastacle(i, j)
                    self.obstaclesArray.append((i, j, o.getVisuel()))
                    carte[i, j] = o.getVisuel()
                    # generation d'obstacle
                elif 0.3 < random.random() < 0.4 and self.nbChild < MAX_CHILD:
                    c = Child(i, j)
                    self.entitysArray.append((i, j, c.getVisuel()))
                    carte[i, j] = c.getVisuel()
                    self.nbChild += 1
                    # generation d'enfant
                elif 0.4 <= random.random() <= 0.45 and self.nbShrek == 0:
                    s = Shrek(i, j)
                    self.entitysArray.append((i, j, s.getVisuel()))
                    carte[i, j] = s.getVisuel()
                    self.nbShrek += 1
                    # generation de shrek
                elif 0.45 <= random.random() <= 0.55:
                    e = Entity(i, j)
                    carte[i, j] = e.getVisuel()
                    # genere de pont
        return carte

    def show_map(self, carte):
        for line in carte:
            for e in line:
                print(f'{visuel[entities[e]]}'.ljust(2), end="")
            print("")


def main():
    map = Map(MAP_HEIGHT, MAP_WIDTH)
    carte = map.create_random_map()
    print(map.getObstacles())
    print(map.getEntitys())
    turn = 0
    while turn < 100:
        # todo appeler move sur les entités

        turn += 1
        pass
    map.show_map(carte)


if __name__ == '__main__':
    main()
