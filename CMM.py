import pygame
import sys
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('/Users/joon/Desktop/Python Game Contest/Python_CMM/Image/펭귄.png')
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init()
        self.display_surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2(-800, 100)

        #gound
        self.ground_surf = pygame.image.load('/Users/joon/Desktop/Python Game Contest/Python_CMM/Image/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

    def custom_draw(self):

        #ground
        ground_offset = self.ground_rect.topleft + self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        #active elements
        for sprite in sorted(self.sprites(), key = lambda sprtie: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, sprite.rect)

#reset pygame
pygame.init()

#screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

#setup
camera_group = pygame.sprite.Group()
Player((640,360), camera_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('#71ddee')

    camera_group.update()
    camera_group.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()