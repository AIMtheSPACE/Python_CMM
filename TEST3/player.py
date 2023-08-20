import pygame
from pygame.sprite import *
from sprites import *
import maps
from sounds import *
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = 400, 300
        self.width, self.height = tilesize, tilesize

        self.x_change = 0
        self.y_change = 0
        self.facing = "down"
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        Player_animation(self)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += player_speed
            self.x_change -= player_speed
            self.facing = "left"
        
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= player_speed
            self.x_change += player_speed
            self.facing = "right"
        
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += player_speed
            self.y_change -= player_speed
            self.facing = "up"
       
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= player_speed
            self.y_change += player_speed
            self.facing = "down"

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_trees("x")
        self.rect.y += self.y_change
        self.collide_trees("y")

        self.x_change = 0
        self.y_change = 0

    def collide_trees(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.trees, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += player_speed
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= player_speed
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.trees, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed
                    self.rect.y = hits[0].rect.bottom
    

    def animate(self):
        Player_animation_animate(self)