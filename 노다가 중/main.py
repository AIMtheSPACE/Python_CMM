import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *

class Button(pygame.sprite.Sprite):
    def __init__(self, image, x, y, callback, scale=1.0):
        super().__init__()
        self.image = pygame.image.load(image)
        if scale != 1.0:
            original_size = self.image.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.callback = callback
        self.is_mouse_over = False
        self.is_clicked = False
        self.prev_mouse_state = False  # 이전 마우스 상태를 추적

        self.mainbutton = pygame.sprite.Group()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.is_mouse_over = True
            if pygame.mouse.get_pressed()[0] and not self.prev_mouse_state:  # Left mouse button clicked
                self.callback()
                self.is_clicked = True
        else:
            self.is_mouse_over = False

        self.prev_mouse_state = pygame.mouse.get_pressed()[0]  # 현재 마우스 상태를 이전 마우스 상태로 업데이트


    def draw(self, surface):
        surface.blit(self.image, self.rect)


# 버튼그리려면 해야 할 것 
# 1. init에 그룹 만들어주기 
# 2. new에 버튼 만들어주기
# 3. draw에 그룹 드로잉 해주기
# 4. 콜백에 쓴 글자와 같은 def콜백 함수 만들어 주기




class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.terrainsheet = Spritesheet("Image/terrain1.png")
        self.character_spritesheet = Spritesheet("Image/character.png")


        self.settingbutton = pygame.sprite.Group()
        self.show_setting = False  
        self.timer_font = pygame.font.SysFont("arialblack", 40)  # 필요에 따라 폰트 크기 조정
        self.period = 1  # 초기 기간 값
        self.min = 1
        self.remaining_time = 60 * self.min  # 기간을 초로 변환한 값
        self.last_time = pygame.time.get_ticks()  # last_time 속성 초기화


        
    def createTilemap(self, tilemap):
        build_map(self, tilemap)

    def new(self, tilemap):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.trees = pygame.sprite.LayeredUpdates()
        self.createTilemap(tilemap)

        # 버튼 생성
        self.button = Button("Image/설정.png", 10, 10, self.setting_callback, 0.01)
        self.settingbutton.add(self.button)

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        
        self.settingbutton.update()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)
        self.settingbutton.draw(self.screen)

        # 카운트 다운 타이머 표시
        timer_text = f"{self.period} Period Break Time / Time left : {self.remaining_time // 60:02}:{self.remaining_time % 60:02}"
        timer_surface = self.timer_font.render(timer_text, True, (255, 235, 2))
        self.screen.blit(timer_surface, (100, -10))  # 필요에 따라 위치 조정

        self.clock.tick(fps)
        pygame.display.update()


    

    def setting_callback(self): # 엔드 게임
        if not self.show_setting:
            # 새로운 버튼 생성
            self.new_button = Button("Image/endgame.png", 100, 100, self.endgame_callback, 0.05)
            self.settingbutton.add(self.new_button)
            
            self.show_setting = True
        else:
            # 버튼 숨기기
            self.settingbutton.remove(self.new_button)
            self.show_setting = False
        
    def endgame_callback(self): 
        # 버튼을 누를 때 동작을 여기에 작성
        self.playing = False
        self.running = False



    def main(self):
        while self.playing:
            self.events()
            self.update()

            # 카운트 다운 타이머 업데이트
            if self.show_setting: # 함수 이름 밖어서 다른 곳에 연결
                current_time = pygame.time.get_ticks()
                if current_time - self.last_time >= 1000:  # 1초마다 업데이트
                    self.last_time = current_time
                    self.remaining_time -= 1
                    if self.remaining_time <= 0:
                        self.show_setting = False #요기도 바꿔야함
                        self.remaining_time = self.period * 60 

            self.draw()



tilemap = maps.world_1.stage_1
game = Game()
game.new(tilemap)
while game.running:
    game.main()

pygame.quit()
sys.exit()