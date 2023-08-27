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

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        self.image = self.game.terrainsheet.get_sprite(0, 96, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.trees
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        tree_1 = [0, 0]
        tree_2 = [31, 0]
        tree_3 = [0, 32]
        tree_4 = [31, 32]
        tree_list = [tree_1, tree_2, tree_3, tree_4]
        tree = random.choice(tree_list)

        self.image = self.game.terrainsheet.get_sprite(tree[0], tree[1], self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.set_colorkey("white")

class Warp(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = warp_layer
        self.groups = self.game.all_sprites, self.game.warps
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width, self.height = tilesize, tilesize
        self.image = self.game.terrainsheet.get_sprite(0, 64, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y