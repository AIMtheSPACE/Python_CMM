from player import *
from sprites import *

def build_map(self, tilemap):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Wooden(self, j, i)
            if column == "P":
                self.Player = Player(self, j, i)
            if column == "C":
                Desk(self, j, i)
            if column == "T":
                Wall(self, j, i)
            if column == "W":
                Warp_Up(self, j, i)
            if column == "D":
                Warp_Down(self, j, i)
            if column == "E":
                Empty(self, j, i)
            if column == "H":
                Hallway(self, j, i)