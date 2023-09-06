import pygame
from config import *
import random
from animation import *
import maps



class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey("black")
        return sprite

class Wooden(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        self.image = self.game.wooden_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

class Hallway(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.hallways
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        self.image = self.game.hallway_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

class Empty(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.emptys
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        self.image = self.game.empty_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.image.set_colorkey("White")

class Desk(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.desks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize

        self.image = self.game.desk_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.set_colorkey("white")

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize

        self.image = self.game.wall_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Closet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.closets
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize

        self.image = self.game.closet_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Warp_Up(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = warp_layer
        self.groups = self.game.all_sprites, self.game.warp_up
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        self.image = self.game.warp_up_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Warp_Down(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = warp_layer
        self.groups = self.game.all_sprites, self.game.warp_down
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        self.image = self.game.warp_down_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Couple(pygame.sprite.Sprite):
    num = 0
    def __init__(self, game, x, y, num):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.couples
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize * 2, tilesize

        self.num = num
        
        if num == 1:
            self.image = self.game.couple1_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 2:
            self.image = self.game.couple2_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 3:
            self.image = self.game.couple3_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 4:
            self.image = self.game.couple4_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 5:
            self.image = self.game.couple5_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 6:
            self.image = self.game.couple6_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 7:
            self.image = self.game.couple7_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 8:
            self.image = self.game.couple8_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 9:
            self.image = self.game.couple9_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif num == 10:
            self.image = self.game.couple10_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y