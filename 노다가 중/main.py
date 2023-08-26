import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *

pygame.init() # 초기화
pygame.display.set_caption("러브캐처 인 청운") # 화면 이름
pygame.display.set_icon(pygame.image.load("Image/청운 로고.png") )

class ChecklistImage(pygame.sprite.Sprite):
    def __init__(self, image_path, scale, center_position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale),
            int(self.image.get_height() * scale)
        ))
        self.rect = self.image.get_rect(center=center_position)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, x, y, callback, scale):
        super().__init__()
        self.image = pygame.image.load(image)
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


# 버튼그리려면 해야 할 것 아래 순서를 다 따라보고, 문제가 발생하면 chat gpt에게 물어볼 것!
# 1. init에 그룹 만들어주기 
# 2. new에 버튼 만들어주기
# 3. draw에 그룹 드로잉 해주기
# 4. 콜백에 쓴 글자와 같은 def콜백 함수 만들어 주기
# 5. event에서 업데이트 해주어야 함. 

# 카운트 다운 시작 방법 정해야함.

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.terrainsheet = Spritesheet("Image/terrain1.png")
        self.character_spritesheet = Spritesheet("Image/character.png")


        self.setting_group = pygame.sprite.Group()
        self.classtime_group = pygame.sprite.Group()
        self.checklist_group = pygame.sprite.Group()
        self.checklistimg_group = pygame.sprite.Group()


        self.show_setting = False  

        self.timer_font = pygame.font.SysFont("arialblack", 40)  # 필요에 따라 폰트 크기 조정
        self.period = 1  # 초기 기간 값
        self.min = 1
        self.remaining_time = 60 * self.min  # 기간을 초로 변환한 값
        self.last_time = pygame.time.get_ticks()  # last_time 속성 초기화
        self.show_checklist = False

        self.page = 1
        self.count_down_start = True


        
    def createTilemap(self, tilemap):
        build_map(self, tilemap)

    def new(self, tilemap):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.trees = pygame.sprite.LayeredUpdates()
        self.createTilemap(tilemap)

        # 버튼 생성
        self.button = Button("Image/설정.png", 10, 10, self.setting_callback, 0.01)
        self.setting_group.add(self.button)

        self.checklist_button = Button("Image/checklist.png", 10, 100, self.checklist_callback, 1)
        self.checklist_group.add(self.checklist_button)

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.page = self.adjust_value(self.page, -1, 1, 4)
                    print(self.page)
                    self.checklistimg_reset()
                     # 페이지가 변하고 체크리스트가 표시 중일 때만 callback 호출
                elif event.key == pygame.K_RIGHT:
                    self.page = self.adjust_value(self.page, 1, 1, 4)
                    print(self.page)
                    self.checklistimg_reset()
                 


        self.setting_group.update()
        self.classtime_group.update()
        self.checklist_group.update()
        self.checklistimg_group.update()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)

        self.setting_group.draw(self.screen)
        self.checklist_group.draw(self.screen)
        self.classtime_group.draw(self.screen)
        self.checklistimg_group.draw(self.screen)
        
        # 카운트 다운 타이머 표시
        timer_text = f"{self.period} Period Break Time / Time left : {self.remaining_time // 60:02}:{self.remaining_time % 60:02}"
        timer_surface = self.timer_font.render(timer_text, True, (255, 235, 2))
        self.screen.blit(timer_surface, (400, -10))  # 필요에 따라 위치 조정

        self.clock.tick(fps)
        pygame.display.update()

    def setting_callback(self): # 엔드 게임
        if not self.show_setting:
            # 새로운 버튼 생성
            self.new_button = Button("Image/endgame.png", 100, 100, self.endgame_callback, 0.05)
            self.setting_group.add(self.new_button)
            
            self.show_setting = True
        else:
            # 버튼 숨기기
            self.setting_group.remove(self.new_button)
            self.show_setting = False

    def checklist_callback(self):
        if self.show_checklist:  # 이미 체크리스트가 표시 중일 때
            self.checklistimg_group.empty()  # 이미지 삭제
            self.show_checklist = False
        else:
            self.checklistimg_reset()
            self.show_checklist = True
            
    def checklistimg_reset(self):
            if self.page == 1:
                image_path = "Image/첵리 1.png"
            elif self.page == 2:
                image_path = "Image/첵리 2.png"
            elif self.page == 3:
                image_path = "Image/첵리 3.png"
            elif self.page == 4:
                image_path = "Image/첵리 4.png"

            image_center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            scaled_image = ChecklistImage(image_path, 0.5, image_center)
            self.checklistimg_group.empty()  # 기존 이미지 삭제
            self.checklistimg_group.add(scaled_image)  # 새로운 이미지 추가
        


    def endgame_callback(self): 
        # 버튼을 누를 때 동작을 여기에 작성
        self.playing = False
        self.running = False



    def show_classtime(self): # 수업 시간 표시 기능
        self.classtime_button = Button("Image/수업 시간에 표시 할 것.png", 100, 100, self.classtime_callback, 0.5)
        self.classtime_group.add(self.classtime_button)
        
    def classtime_callback(self):
        self.classtime_group.remove(self.classtime_button)
        self.count_down_start = True

    def adjust_value(self, value, change, min_value, max_value):
            new_value = value + change
            return max(min(new_value, max_value), min_value)


    def draw_scaled_image(self, image, scale, center_position):
        self.image = pygame.image.load(image)  # 이미지 확장자 추가
        scaled_image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale),
            int(self.image.get_height() * scale)
        ))
        scaled_image_rect = scaled_image.get_rect(center=center_position)
        self.screen.blit(scaled_image, scaled_image_rect.topleft)


    def main(self):
        while self.playing:
            self.events()
            self.update()

            # 카운트 다운 타이머 업데이트
            if self.count_down_start: # 함수 이름 밖어서 다른 곳에 연결
                current_time = pygame.time.get_ticks()
                if current_time - self.last_time >= 1000:  # 1초마다 업데이트
                    self.last_time = current_time
                    self.remaining_time -= 1
                    if self.remaining_time <= 0:
                        self.count_down_start = False #요기도 바꿔야함
                        self.remaining_time = 60 * self.min
                        self.period += 1 # 교시 숫자 올리기.
                        # 요기에 카운트 다운 바로 실행하는 코드 필요함(차차))
                        self.show_classtime()

            self.draw()



tilemap = maps.world_1.stage_1
game = Game()
game.new(tilemap)
while game.running:
    game.main()

pygame.quit()
sys.exit()