import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *
import time


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.terrainsheet = Spritesheet("Image/terrain1.png")
        self.character_spritesheet = Spritesheet("Image/character.png")

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

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)
        self.clock.tick(fps)

        pygame.display.update()

    def _time(self):
        _font = pygame.font.SysFont(None, 100)
        start_time = int(time.time())
        remain_time = 0
        YELLOW = (255, 255, 0)

        while(True):
            remain_time = 60 - (int(time.time()) - start_time)
            remain_time_image = _font.render('Time {}'.format(remain_time), True, YELLOW)
            self.screen.blit(remain_time_image, (win_width - 20 - remain_time_image.get_rect(), 20))

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self._time()

tilemap = maps.world_1.stage_1
game = Game()
game.new(tilemap)
while game.running:
    game.main()

pygame.quit()
sys.exit()