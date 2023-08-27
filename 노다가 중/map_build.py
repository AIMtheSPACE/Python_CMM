from player import *
from sprites import *

def build_map(self, tilemap):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(self, j, i)
            if column == "P":
                self.Player = Player(self, j, i)
            if column == "T":
                Tree(self, j, i)
            if column == "W":
                Warp(self, j, i)