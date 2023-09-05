from player import *
from sprites import *
from config import *

def build_map(self, tilemap):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Wooden(self, j+a, i+b)
            if column == "P":
                self.Player = Player(self, j, i)
            if column == "B":
                Desk(self, j+a, i+b)
            if column == "T":
                Wall(self, j+a, i+b)
            if column == "U":
                Warp_Up(self, j+a, i+b)
            if column == "D":
                Warp_Down(self, j+a, i+b)
            if column == "0":
                Empty(self, j+a, i+b)
            if column == "H":
                Hallway(self, j+a, i+b)
            if column == "C":
                Couple(self, j+a, i+b)