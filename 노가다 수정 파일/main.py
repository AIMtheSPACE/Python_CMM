import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width, height, callback):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the button image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.callback = callback
        self.clicked = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                self.callback()
        else:
            self.clicked = False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.terrainsheet = Spritesheet("Image/terrain1.png")
        self.character_spritesheet = Spritesheet("Image/character.png")
        button_width = 100  # Set the desired button width
        button_height = 50  # Set the desired button height
        self.checklist_button = ImageButton(20, 20, "Image/파일.png", button_width, button_height, self.quit_game)

        self.buttons = pygame.sprite.Group() # Initialize the buttons group



    def createTilemap(self, tilemap):
        build_map(self, tilemap)

    def new(self, tilemap):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.trees = pygame.sprite.LayeredUpdates()
        self.createTilemap(tilemap)
        self.buttons.add(self.checklist_button)  # Add the exit button to the buttons group


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
        self.buttons.draw(self.screen)  # Draw the buttons group
        self.clock.tick(fps)
        pygame.display.update()


        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def quit_game(self):
        self.playing = False
        self.running = False

tilemap = maps.world_1.stage_1
game = Game()
game.new(tilemap)
while game.running:
    game.main()

pygame.quit()
sys.exit()

