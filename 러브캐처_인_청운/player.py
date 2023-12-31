import pygame
from pygame.sprite import *
from sprites import *
import maps
import random
from config import*

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x, self.y = 624, 434
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
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += player_speed
            self.x_change -= player_speed
            self.facing = "left"
        
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= player_speed
            self.x_change += player_speed
            self.facing = "right"
        
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += player_speed
            self.y_change -= player_speed
            self.facing = "up"
       
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= player_speed
            self.y_change += player_speed
            self.facing = "down"

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_walls("x")
        self.collide_desks("x")
        self.collide_closets("x")
        self.collide_warp_up("x")
        self.collide_warp_down("x")
        self.collide_couples("x")
        self.collide_students("x")
        self.collide_umbrellas("x")
        self.collide_white("x")
        self.rect.y += self.y_change
        self.collide_walls("y")
        self.collide_desks("y")
        self.collide_closets("y")
        self.collide_warp_up("y")
        self.collide_warp_down("y")
        self.collide_couples("y")
        self.collide_students("y")
        self.collide_umbrellas("y")
        self.collide_white("y")

        self.x_change = 0
        self.y_change = 0

    def collide_walls(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
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
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed
                    self.rect.y = hits[0].rect.bottom

    def collide_desks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.desks, False)
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
            hits = pygame.sprite.spritecollide(self, self.game.desks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed
                    self.rect.y = hits[0].rect.bottom

    def collide_closets(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.closets, False)
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
            hits = pygame.sprite.spritecollide(self, self.game.closets, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed
                    self.rect.y = hits[0].rect.bottom
    
    def collide_warp_up(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.warp_up, False)
            if hits:
                self.game.change_tilemap_up()  # 타일맵을 변경하는 메서드 호출

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.warp_up, False)
            if hits:
                self.game.change_tilemap_up()

    def collide_warp_down(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.warp_down, False)
            if hits:
                self.game.change_tilemap_down()

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.warp_down, False)
            if hits:
                self.game.change_tilemap_down()


    def collide_couples(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.couples, False)
            if hits:
                couple_num = hits[0].num 
                self.game.couplecaught(couple_num) 

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.couples, False)
            if hits:
                couple_num = hits[0].num
                self.game.couplecaught(couple_num)
                
        # hits 리스트의 첫 번째 요소에서 num을 가져온다.
        # couplecaught 전달

    def collide_students(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.students, False)
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
            hits = pygame.sprite.spritecollide(self, self.game.students, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed
                    self.rect.y = hits[0].rect.bottom

    def collide_umbrellas(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.umbrellas, False)
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
            hits = pygame.sprite.spritecollide(self, self.game.umbrellas, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed
                    self.rect.y = hits[0].rect.bottom
    
    def collide_white(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.white, False)
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
            hits = pygame.sprite.spritecollide(self, self.game.white, False)
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