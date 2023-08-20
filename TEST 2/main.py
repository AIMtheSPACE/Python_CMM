import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *
from defi import*


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.terrainsheet = Spritesheet("Image/terrain1.png")
        self.character_spritesheet = Spritesheet("Image/character.png")
        self.setting_button = Button(30, 60, setting_image, 0.02)
        self.checklist_button = Button(100, 30, checklist_image, 1)
        self.show_checklist_overlay = False  # checklist 상태 변수 추가
        self.show_right_arrow = False
        self.show_left_arrow = False


    def createTilemap(self, tilemap):
        build_map(self, tilemap)

    def new(self, tilemap):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.trees = pygame.sprite.LayeredUpdates()
        self.createTilemap(tilemap)

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

        if self.setting_button.draw(self.screen):
            show_settings_overlay = not show_settings_overlay

        if self.checklist_button.draw(self.screen) or (show_checklist_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_l):
            show_checklist_overlay = not show_checklist_overlay
            show_right_arrow = not show_right_arrow
            show_left_arrow = not show_left_arrow
            
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)
        self.clock.tick(fps)
        self.setting_button.draw(self.screen)
        self.checklist_button.draw(self.screen)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

