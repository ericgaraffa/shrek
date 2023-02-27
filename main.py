import numpy as np
import random

MAP_HEIGHT = 32
MAP_WIDTH = 32

directions = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

entities = {
    0: "sol",
    1: "pont",
    2: "arbre",
    3: "rocher",
    4: "eau",
    5: "enfant",
    6: "troll"
}

visuel = {
    "sol": ".",
    "pont": "=",
    "arbre": "♣",
    "rocher": "♦",
    "eau": "o",
    "enfant": "e",
    "troll": "X"
}


class Entity:
    def __init__(self, x, y):
        self.visuel = "v"
        self.x = x
        self.y = y


class Child(Entity):
    def __init__(self, x, y):
        super.__init__(x, y)
        self.visuel = random.choice["e1", "e2", "e3"]

    def move(self, carte):
        h, w = carte.shape()
        for dx, dy in directions.values():
            if 0 <= self.x + dx < h and 0 <= self.y + dy < w and carte[self.x + dx, self.y + dy] < 2:  # pas d'obstacle
                self.x += dx
                self.y += dy

                # todo mettre à jour la carte

                return carte
        return carte


def create_random_map(h, w):
    carte = np.zeros((h, w), dtype=int)

    # generation des entites
    for i in range(h):
        for j in range(w):
            if i < 2 or i > h - 3 or j < 2 or j > w - 3:
                carte[i, j] = 2
            # generer des arbres
            elif random.random() < 0.1:
                carte[i, j] = random.choice([2, 3, 4, 5])

    return carte


def show_map(carte):
    for line in carte:
        for e in line:
            print(f'{visuel[entities[e]]}'.ljust(2), end="")
        print("")


def main():
    carte = create_random_map(MAP_HEIGHT, MAP_WIDTH)

    turn = 0
    while turn < 100:
        # todo appeler move sur les entités
        turn += 1
        pass
    show_map(carte)


if __name__ == '__main__':
    main()
