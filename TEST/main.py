import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *
from countdown import *

pygame.init()
pygame.display.set_caption("러브캐처 인 청운") # 화면 이름
pygame.display.set_icon(pygame.image.load("Image/청운 로고.png") )

# 버튼 클래스
class Button:
    def __init__(self, game, image, x, y, action):
        self.game = game
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos) and mouse_pressed:
            if not self.clicked:
                self.clicked = True
                return self.action
        else:
            self.clicked = False
        return None
    

class Game:
    def scale_image(self, image, scale_factor):
        width = int(image.get_width() * scale_factor)
        height = int(image.get_height() * scale_factor)
        return pygame.transform.scale(image, (width, height))

    def load_scaled_image(self, image_path, scale_factor):
        image = pygame.image.load(image_path).convert_alpha()
        return self.scale_image(image, scale_factor)
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.terrainsheet = Spritesheet("Image/terrain1.png")
        self.character_spritesheet = Spritesheet("Image/character.png")

        # 버튼 생성
        self.count = 0  # 카운트 변수 초기화
        self.state = "background"  # "background", "intro", "playing"

        self.menu_image = self.load_scaled_image('Image/아이콘.png', 0.5)
        self.setting_image = self.load_scaled_image('Image/설정.png', 0.05)
        self.checklist_image = self.load_scaled_image('Image/파일.png', 1)
        self.classtime_image = self.load_scaled_image('Image/수업 시간에 표시 할 것.png', 1)
        self.endgame_image = self.load_scaled_image('Image/endgame.png', 1)

        self.menu_button = Button(self, self.menu_image, 10, 10, "start")
        self.setting_button = Button(self, self.setting_image, 100, 10, "start")
        self.checklist_button = Button(self, self.checklist_image, 500, 10, "start")
        self.classtime_button = Button(self, self.classtime_image, 0, 0, "start")
        self.endgame_button = Button(self, self.classtime_image, 100, 300, "endgame")
     

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
        show_setting = False
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)

        # 버튼 그리기
        action = self.menu_button.check_click()
        action = self.endgame_button.check_click()

        if action == "start":
            self.count += 1
            show_setting = not show_setting
        if show_setting:
            self.endgame_button.draw(self.screen)
            if action == "endgame":
                pygame.quit()
                sys.exit()

        self.menu_button.draw(self.screen)
        self.checklist_button.draw(self.screen)
        self.setting_button.draw(self.screen)

        font = pygame.font.SysFont("arialblack", 24)
        text_surface = font.render(f"Count: {self.count}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(10, 10))
        self.screen.blit(text_surface, text_rect)

        pygame.display.update()

    def show_background(self):
        self.screen.fill((0, 0, 0))
        background_image = pygame.image.load("Image/배경화면.jpeg")
        self.screen.blit(background_image, (0, 0))
        pygame.display.update()

    def show_intro(self):
        self.screen.fill((0, 0, 0)) 
        intro_image = pygame.image.load("Image/intro.png")
        self.screen.blit(intro_image, (0, 0))
        pygame.display.update()

    def main(self):
        while self.running:
            if self.state == "background":
                self.show_background()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.state = "intro"
            elif self.state == "intro":
                self.show_intro()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.state = "playing"
                        tilemap = maps.world_1.stage_1
                        self.new(tilemap)
            elif self.state == "playing":
                self.events()
                self.update()
                self.draw()
             
            pygame.display.flip()
            self.clock.tick(fps)


        pygame.quit()
        sys.exit()


# 게임 시작
tilemap = maps.world_1.stage_1
game = Game()
game.new(tilemap)
while game.running:
    game.main()

pygame.quit()
sys.exit()

