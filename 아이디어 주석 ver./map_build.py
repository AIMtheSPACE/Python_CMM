from player import *
from sprites import *

def build_map(self, tilemap):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row): # 또는 여기 값
            Wooden(self, j, i)
            if column == "P":
                self.Player = Player(self, j, i)
            if column == "B":
                Desk(self, j, i)
            if column == "T":
                Wall(self, j, i)
            if column == "U":
                Warp_Up(self, j, i)
            if column == "D":
                Warp_Down(self, j, i)
            if column == "0":
                Empty(self, j, i)
            if column == "H":
                Hallway(self, j, i)
            if column == "C":
                Couple(self, j, i)