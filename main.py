import numpy as np
import random
import time

#Global var
MAP_HEIGHT = 16
MAP_WIDTH = 16
MAX_CHILD = 10
DIST_SHREK = 2

directions = {"right": (0, 1), "left": (0, -1), "up": (-1, 0), "down": (1, 0)}

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
    "sol": ".",
    "pont": "=",
    "arbre": "■",
    "rocher": "■",
    "eau": "■",
    "enfant": "e",
    "shrek": "X",
    "standard": "C",
    "fille": "C",
    "garçon": "C",
    "chapeau": "C",
    "instrument": "C",
    "tombe": "!",
    "poussière": "!",
    "ossement": "!",
    "rien": "!"
}


def distance(x, y, a, b):
    return abs(x - a) + abs(y - b)


class Entity:
    def __init__(self, x, y):
        self.id = 1
        self.x = x
        self.y = y
        self.cross = 1

    def getVisuel(self):
        return visuel[entities[self.id]]

    def move(self, carte, xShrek=None, yShrek=None):
        return

    def death(self):
        return


class Child(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_dead = 0
        self.id = random.choice([5, 6, 7, 8, 9])
        self.visuel = visuel[entities[self.id]]
        self.cross = 0

    def __str__(self):
        return f"Child: x={self.x} y={self.y} visuel:'{self.getVisuel()}' "

    def move(self, carte, xShrek, yShrek):
        if abs(self.x - xShrek) + abs(self.y - yShrek) <= DIST_SHREK:
            return

        if self.is_dead == 1:
            return

        h, w = carte.h, carte.w
        for dx, dy in directions.values():
            # pas hors map && pas d'obstacle
            if 0 <= self.x + dx < h and 0 <= self.y + dy < w and carte.can_move_to(self.x + dx, self.y + dy):
                # print("Move:", self.x, self.y, '->', self.x + dx, self.y + dy)
                self.x += dx
                self.y += dy
                return
        return

    def getPos(self):
        return self.x, self.y

    def death(self):
        if self.is_dead == 1:
            return
        print("Enfant mort", self.x, self.y)
        self.is_dead = 1
        self.id = random.choice([10, 11, 12, 13])
        self.visuel = visuel[entities[self.id]]
        self.cross = 1
        return


class Shrek(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 14
        self.cross = 0

    def __str__(self):
        return f"Shrek: x={self.x} y={self.y} visuel:'{self.getVisuel()}' "

    def eat(self, Child):
        Child.death()
        return

    def getPos(self):
        return self.x, self.y

    def move(self, carte, xShrek=None, yShrek=None, children_positions=[]):
        print("nb children =", len(children_positions))
        h, w = carte.h, carte.w

        if children_positions:
            # trie des enfants du plus proche au plus loin
            children_positions.sort(key=lambda e: distance(self.x, self.y, e[0], e[1]))

            # le plus proche est le premier
            closest = children_positions[0]
            print("> Enfant le plus proche en:", closest, "shrek pos:", self.x, self.y)

            # ecart à l'enfant
            dx = closest[0] - self.x
            dy = closest[1] - self.y

            print("offset enfant:", dx, dy)

            # meilleure direction:
            if abs(dx) > 0 and abs(dx) >= abs(dy):
                # 1 || -1
                dx = int(dx / abs(dx))
                dy = 0
                print("test move en ", self.x + dx, self.y + dy)
                if 0 <= self.x + dx < h and 0 <= self.y + dy < w and carte.can_move_to(self.x + dx, self.y + dy,
                                                                                       shrek=True):
                    print("Shrek move > dx:", dx, "dy:", dy, self.x, self.y, "->", self.x + dx, self.y + dy)
                    self.x += dx
                    self.y += dy
                    return

            if abs(dy) > 0:
                # 1 || -1
                dx = 0
                dy = int(dy / abs(dy))
                print("test move en ", self.x + dx, self.y + dy)
                if 0 <= self.x + dx < h and 0 <= self.y + dy < w and carte.can_move_to(self.x + dx, self.y + dy,
                                                                                       shrek=True):
                    print("Shrek move > dx:", dx, "dy:", dy, self.x, self.y, "->", self.x + dx, self.y + dy)
                    self.x += dx
                    self.y += dy
                    return

        l = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        random.shuffle(l)
        for dx, dy in l:
            # print("check pos:", self.x + dx, self.y + dy,
            #       0 <= self.x + dx < h and 0 <= self.y + dy < w and carte.can_move_to(self.x + dx, self.y + dy, shrek=True))
            # pas hors map && pas d'obstacle
            if 0 <= self.x + dx < h and 0 <= self.y + dy < w and carte.can_move_to(self.x + dx, self.y + dy, shrek=True):
                print("Shrek move > dx:", dx, "dy:", dy, 'move random')
                self.x += dx
                self.y += dy

                return
        # print("Shrek kéblo")
        return


class Obstacle(Entity):
    def __init__(self, x, y, id=None):
        super().__init__(x, y)
        if id is None:
            self.id = random.choice([2, 3, 4])
        else:
            self.id = id

        self.cross = 0

    def __str__(self):
        return f"Obstacle: x={self.x} y={self.y} visuel:'{self.getVisuel()}' "


class Bridge(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 1
        self.cross = 1

    def __str__(self):
        return f"Bridge: x={self.x} y={self.y} visuel:'{self.getVisuel()}' "


class Map:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.entities = []
        self.shrek = None
        self.nbChild = len(self.getPosChild())
        self.create_random_map()

    # Obstacle ou non
    def can_move_to(self, x, y, shrek=False):
        for e in self.entities:
            if e.x == x and e.y == y:
                if shrek:
                    # si c'est un enfant on peut y aller et ça mange
                    return e.id in [0, 1, 5, 6, 7, 8, 9,10, 11, 12, 13]
                # s'il y a une entité, alors on retourne si elle est traversable ou non
                return e.cross
        # s'il n'y a pas d'entité on peut passer
        return True

    def getPosChild(self):
        if not self.entities:
            return []
        children = [(e.x, e.y) for e in self.entities if e.id in [5, 6, 7, 8, 9]]
        return children

    def create_random_map(self):
        # generation des entites
        for i in range(self.h):
            for j in range(self.w):
                if i < 2 or i > self.h - 3 or j < 2 or j > self.w - 3:
                    # genere arbre du contour
                    self.entities.append(Obstacle(i, j, id=2))
                elif random.random() < 0.15:
                    # generation d'obstacle
                    self.entities.append(Obstacle(i, j))
                elif 0.3 < random.random() < 0.4 and self.nbChild < MAX_CHILD:
                    # generation d'enfant
                    self.entities.append(Child(i, j))
                    self.nbChild += 1
                elif 0.4 <= random.random() <= 0.45 and self.shrek is None:
                    # generation de shrek
                    self.shrek = Shrek(i, j)
                elif 0.45 <= random.random() <= 0.55:
                    # genere de pont
                    self.entities.append(Bridge(i, j))
        # print("map created:", self.shrek)

    def show_map(self):
        carte = np.zeros((self.h, self.w), dtype=int)

        for e in self.entities:
            carte[e.x, e.y] = e.id

        carte[self.shrek.x, self.shrek.y] = self.shrek.id

        for line in carte:
            for e in line:
                print(f'{visuel[entities[e]]}'.ljust(2), end="")
            print("")
        print("")

    def move_entities(self):
        xShrek, yShrek = self.shrek.getPos()
        #Bouge entities
        for entity in self.entities:
            entity.move(self, xShrek, yShrek)
        #Bouge shrek
        self.shrek.move(self, children_positions=self.getPosChild())
        self.shrek_eats_on(self.shrek.x, self.shrek.y)

    def shrek_eats_on(self, x, y):
        for e in self.entities:
            if e.x == x and e.y == y:
                e.death()
                self.nbChild = len(self.getPosChild())
                return

def main():
    map = Map(MAP_HEIGHT, MAP_WIDTH)
    turn = 0
    print(f"turn {turn}:")
    map.show_map()
    while turn < 100 and map.nbChild > 0:
        turn += 1
        print(f"turn {turn}:")
        map.move_entities()
        map.show_map()
        # time.sleep(1)

    print(map.nbChild, "children left")


if __name__ == '__main__':
    main()
