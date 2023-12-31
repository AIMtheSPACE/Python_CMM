from player import *
from sprites import *
from config import *

def build_map(self, tilemap):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Hallway(self, j+a, i+b)
            if column == "P":
                self.Player = Player(self, j, i)
            
            #의자 방향별 배치
            if column == "W":
                Desk(self, j+a, i+b, 1)
            if column == "X":
                Desk(self, j+a, i+b, 2)
            if column == "Y":
                Desk(self, j+a, i+b, 3)
            if column == "Z":
                Desk(self, j+a, i+b, 4)
            if column == "w":
                Desk(self, j+a, i+b, 5)
            if column == "x":
                Desk(self, j+a, i+b, 6)
            if column == "y":
                Desk(self, j+a, i+b, 7)
            if column == "z":
                Desk(self, j+a, i+b, 8)
            
            if column == "T":
                Wall(self, j+a, i+b)
            if column == "R":
                Stair(self, j+a, i+b)
            if column == "U":
                Warp_Up(self, j+a, i+b)
            if column == "D":
                Warp_Down(self, j+a, i+b)
            if column == "0":
                Empty(self, j+a, i+b)
            if column == "H":
                Wooden(self, j+a, i+b)
            if column == "S":
                Closet(self, j+a, i+b)
            if column == "I":
                White(self, j+a, i+b)
            
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
            
            # 일반 학생 배치
            if column == "a":
                Student(self, j+a, i+b, 1)
            if column == "b":
                Student(self, j+a, i+b, 2)
            if column == "c":
                Student(self, j+a, i+b, 3)
            if column == "d":
                Student(self, j+a, i+b, 4)
            if column == "e":
                Student(self, j+a, i+b, 5)
            if column == "f":
                Student(self, j+a, i+b, 6)
            
            if column == "g":
                Student(self, j+a, i+b, 7)
            if column == "h":
                Student(self, j+a, i+b, 8)
            if column == "i":
                Student(self, j+a, i+b, 9)
            if column == "j":
                Student(self, j+a, i+b, 10)
            if column == "k":
                Student(self, j+a, i+b, 11)
            if column == "l":
                Student(self, j+a, i+b, 12)

            # 우산 배치
            if column == "o":
                Umbrella(self, j+a, i+b, 1)
            if column == "p":
                Umbrella(self, j+a, i+b, 2)
            if column == "q":
                Umbrella(self, j+a, i+b, 3)
            if column == "r":
                Umbrella(self, j+a, i+b, 4)
            if column == "s":
                Umbrella(self, j+a, i+b, 5)
            if column == "t":
                Umbrella(self, j+a, i+b, 6)

def build_map_end(self, tilemap):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Hallway(self, j, i)
            if column == "P":
                self.Player = Player(self, j, i)
            if column == "T":
                Wall(self, j, i)
            
            # 커플 배치
            if column == "1":
                Couple(self, j, i, 11)
            if column == "2":
                Couple(self, j, i, 12)
            if column == "3":
                Couple(self, j, i, 13)
            if column == "4":
                Couple(self, j, i, 14)
            if column == "5":
                Couple(self, j, i, 15)
            if column == "6":
                Couple(self, j, i, 16)
            if column == "7":
                Couple(self, j, i, 17)
            if column == "8":
                Couple(self, j, i, 18)
            if column == "9":
                Couple(self, j, i, 19)
            if column == "*":
                Couple(self, j, i, 20)