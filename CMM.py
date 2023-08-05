import pygame
import sys
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ.png')
        self.rect = self.image.get_rect(center=pos)
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
        super().__init__()  # Fixed: added parentheses to call superclass constructor
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2  # Fixed: get_size() instead of get_sixe()
        self.half_h = self.display_surface.get_size()[1] // 2  # Fixed: get_size() instead of get_sixe()

        # Ground
        self.ground_surf = pygame.image.load('/Users/joon/Desktop/Python Game Contest/Python_CMM/Image/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h 

    def custom_draw(self, player):  # Fixed: typo, should be 'custom_draw' instead of 'center_terget_camera'
        self.center_target_camera(player)  # Fixed: typo, should be 'center_target_camera'

        # Ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)  # Fixed: use 'offset_pos' instead of 'sprite.rect'

# Reset pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Setup
camera_group = Camera()  # Fixed: create Camera object instead of pygame.sprite.Group()
player = Player((640, 360), camera_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('#71ddee')

    camera_group.update()
    camera_group.custom_draw(player)  # Fixed: use custom_draw instead of draw
    pygame.display.update()
    clock.tick(60)