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
            
            # 커플 배치
            if column == "1":
                Couple(self, j+a, i+b, 1)
            if column == "2":
                Couple(self, j+a, i+b, 2)
            if column == "3":
                Couple(self, j+a, i+b, 3)
            if column == "4":
                Couple(self, j+a, i+b, 4)
            if column == "5":
                Couple(self, j+a, i+b, 5)
            if column == "6":
                Couple(self, j+a, i+b, 6)
            if column == "7":
                Couple(self, j+a, i+b, 7)
            if column == "8":
                Couple(self, j+a, i+b, 8)
            if column == "9":
                Couple(self, j+a, i+b, 9)
            if column == "*":
                Couple(self, j+a, i+b, 10)