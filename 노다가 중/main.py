import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *
import pygame.mixer

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
        self.desk_spritesheet = Spritesheet("Image/tile desk.png")
        self.hallway_spritesheet = Spritesheet("Image/tile hallway.jpeg")
        self.closet_spritesheet = Spritesheet("Image/tile shoes closet.jpeg")
        self.wooden_spritesheet = Spritesheet("Image/tile wooden.jpeg")
        self.wall_spritesheet = Spritesheet("Image/tile wall.png")
        self.warp_up_spritesheet = Spritesheet("Image/tile up.jpeg")
        self.warp_down_spritesheet = Spritesheet("Image/tile down.jpeg")
        self.character_spritesheet = Spritesheet("Image/character.png")
        self.empty_spritesheet = Spritesheet("Image/tile black.png")


        self.setting_group = pygame.sprite.Group()
        self.classtime_group = pygame.sprite.Group()
        self.ending_group = pygame.sprite.Group() 
        self.checklist_group = pygame.sprite.Group()
        self.checklistimg_group = pygame.sprite.Group()
        self.mute_group = pygame.sprite.Group()

        self.show_setting = False  

        self.timer_font = pygame.font.SysFont("arialblack", 40)  # 필요에 따라 폰트 크기 조정
        self.period = 1  # 초기 기간 값
        self.min = 1
        self.remaining_time = 60 * self.min  # 기간을 초로 변환한 값
        self.last_time = pygame.time.get_ticks()  # last_time 속성 초기화
        self.show_checklist = False
        self.show_vol = True
        self.page = 1
        self.stage = 1
        self.count_down_start = True

        self.tilemap = None
    
        # 음악 관련
        pygame.mixer.init()  # Initialize mixer
        pygame.mixer.music.load("Song/배달의민족 - 배달은 자신있어.mp3")  # Load background music
        pygame.mixer.music.set_volume(0)  # Set music volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)
        self.button_click_sound = pygame.mixer.Sound("Song/Tiny Button Push Sound.mp3")


        
    def createTilemap(self, tilemap):
        self.all_sprites.empty()  # 기존 스프라이트 삭제
        self.desks.empty()  # 기존 책상 스프라이트 삭제
        self.walls.empty()  # 기존 벽 스프라이트 삭제
        self.closets.empty()  # 기존 신발장 스프라이트 삭제
        self.warp_up.empty()  # 기존 워프 스프라이트 삭제
        self.warp_down.empty()  # 기존 워프 스프라이트 삭제
        self.emptys.empty()
        self.hallways.empty()
        build_map(self, tilemap)  

    def new(self, tilemap):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.desks = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        self.closets = pygame.sprite.LayeredUpdates()
        self.warp_up = pygame.sprite.LayeredUpdates()
        self.warp_down = pygame.sprite.LayeredUpdates()
        self.emptys = pygame.sprite.LayeredUpdates()
        self.hallways = pygame.sprite.LayeredUpdates()
        self.tilemap = tilemap
        self.createTilemap(tilemap)

        # 버튼 생성
        self.button = Button("Image/설정.png", 10, 10, self.setting_callback, 1)
        self.setting_group.add(self.button)

    def change_tilemap_up(self):
        self.stage += 1
        if self.stage == 1:
            self.tilemap = maps.world_1.stage_1
        elif self.stage == 2:
            self.tilemap = maps.world_1.stage_2
        elif self.stage == 3:
            self.tilemap = maps.world_1.stage_3
        elif self.stage == 4:
            self.tilemap = maps.world_1.stage_4
        elif self.stage == 5:
            self.tilemap = maps.world_1.stage_5

        self.createTilemap(self.tilemap)
    def change_tilemap_down(self):
        self.stage -= 1
        if self.stage == 1:
            self.tilemap = maps.world_1.stage_1
        elif self.stage == 2:
            self.tilemap = maps.world_1.stage_2
        elif self.stage == 3:
            self.tilemap = maps.world_1.stage_3
        elif self.stage == 4:
            self.tilemap = maps.world_1.stage_4
        elif self.stage == 5:
            self.tilemap = maps.world_1.stage_5
        
        self.createTilemap(self.tilemap)
        

        # W는 계단 업, 또 다른 알파벳은 계단 다운 등으로 하면 될 듯


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.page = self.adjust_value(self.page, -1, 1, 10)
                    print(self.page)
                    self.checklistimg_reset()
                     # 페이지가 변하고 체크리스트가 표시 중일 때만 callback 호출
                elif event.key == pygame.K_RIGHT:
                    self.page = self.adjust_value(self.page, 1, 1, 10)
                    print(self.page)
                    self.checklistimg_reset()
                elif event.key == pygame.K_UP:
                    if self.show_checklist:  # 이미 체크리스트가 표시 중일 때
                        self.checklistimg_group.empty()  # 이미지 삭제
                        self.show_checklist = False
                    else:
                        self.checklistimg_reset()
                        self.show_checklist = True
                    
                 


        self.setting_group.update()
        self.classtime_group.update()
        self.ending_group.update()
        self.checklist_group.update()
        self.checklistimg_group.update()
        self.mute_group.update()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)

        self.setting_group.draw(self.screen)
        self.checklist_group.draw(self.screen)
        self.ending_group.draw(self.screen)
        self.checklistimg_group.draw(self.screen)
        self.mute_group.draw(self.screen)
        self.classtime_group.draw(self.screen)
        
        # 카운트 다운 타이머 표시
        timer_text = f"{self.period} Period Break Time / Time left : {self.remaining_time // 60:02}:{self.remaining_time % 60:02}"
        timer_surface = self.timer_font.render(timer_text, True, (255, 235, 2))
        self.screen.blit(timer_surface, (400, -10))  # 필요에 따라 위치 조정

        floor_text = f"Floor {self.stage}"
        floor_surface = self.timer_font.render(floor_text, True, (255, 235, 2))
        self.screen.blit(floor_surface, (10, 850))  # 필요에 따라 위치 조정

        self.clock.tick(fps)
        pygame.display.update()

    def setting_callback(self): # 엔드 게임
        self.button_click_sound.play()

        if not self.show_setting:
            # 새로운 버튼 생성
            self.new_button = Button("Image/endgame.png", 100, 10, self.endgame_callback, 0.05)
            self.setting_group.add(self.new_button)
            
            self.show_setting = True

            self.checklist_button = Button("Image/checklist.png", 10, 100, self.checklist_callback, 2)
            self.checklist_group.add(self.checklist_button)

            self.mute_button = Button("Image/mute.jpeg", 100, 100, self.mute_callback, 0.1)
            self.mute_group.add(self.mute_button)

        else:
            # 버튼 숨기기
            self.setting_group.remove(self.new_button)
            self.checklist_group.remove(self.checklist_button)
            self.mute_group.remove(self.mute_button)
            self.show_setting = False

    def checklist_callback(self):
        self.button_click_sound.play()

        if self.show_checklist:  # 이미 체크리스트가 표시 중일 때
            self.checklistimg_group.empty()  # 이미지 삭제
            self.show_checklist = False
        else:
            self.checklistimg_reset()
            self.show_checklist = True
            
    def checklistimg_reset(self):
            if self.page == 1:
                image_path = "Image/checklist_1.png"
            elif self.page == 2:
                image_path = "Image/checklist_2.png"
            elif self.page == 3:
                image_path = "Image/checklist_3.png"
            elif self.page == 4:
                image_path = "Image/checklist_4.png"
            elif self.page == 5:
                image_path = "Image/checklist_5.png"
            elif self.page == 6:
                image_path = "Image/checklist_6.png"
            elif self.page == 7:
                image_path = "Image/checklist_7.png"
            elif self.page == 8:
                image_path = "Image/checklist_8.png"
            elif self.page == 9:
                image_path = "Image/checklist_9.png"
            elif self.page == 10:
                image_path = "Image/checklist_10.png"
           

            image_center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            scaled_image = ChecklistImage(image_path, 1, image_center)
            self.checklistimg_group.empty()  # 기존 이미지 삭제
            self.checklistimg_group.add(scaled_image)  # 새로운 이미지 추가
        
    def mute_callback(self):
        self.button_click_sound.play()

        if self.show_vol:  # 이미 체크리스트가 표시 중일 때
            pygame.mixer.music.set_volume(0.5)
            self.show_vol = False
        else:
            pygame.mixer.music.set_volume(0.0)
            self.show_vol = True

    def endgame_callback(self): 
        self.button_click_sound.play()

        # 버튼을 누를 때 동작을 여기에 작성
        self.playing = False
        self.running = False



    def show_classtime(self): # 수업 시간 표시 기능
        self.classtime_button = Button("Image/수업 시간에 표시 할 것.png", 0, 0, self.classtime_callback, 0.7)
        self.classtime_group.add(self.classtime_button)

    def show_ending(self): # 엔딩 코드 여기다 !!!! 수정 필
        self.ending_button = Button("Image/ending.png", 100, 100, self.endgame_callback, 0.5)
        self.ending_group.add(self.ending_button)
        
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

    def show_intro_images(self):
        intro_images = ["Image/배경화면.jpeg", "Image/intro.png", "Image/대지 1.png"] # 첫번째 
        current_intro_index = 0
        total_intro_images = len(intro_images)
        show_intro = True

        while show_intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_intro_index += 1
                        if current_intro_index >= total_intro_images:
                            show_intro = False

            if current_intro_index < total_intro_images:
                intro_image = pygame.image.load(intro_images[current_intro_index])
                intro_image = pygame.transform.scale(intro_image, (win_width, win_height))
                self.screen.blit(intro_image, (0, 0))
                pygame.display.flip()
                self.clock.tick(60)
            else:
                show_intro = False

    def main(self):
        self.show_intro_images()

        while self.playing:
            self.events()
            self.update()

            # 카운트 다운 타이머 업데이트
            if self.count_down_start: # 함수 이름 밖어서 다른 곳에 연결
                current_time = pygame.time.get_ticks()
                if current_time - self.last_time >= 1000: # 1초마다 업데이트
                    self.last_time = current_time
                    self.remaining_time -= 1
                    if self.remaining_time <= 0:
                        if self.period == 3: # 4교시 쉬는 시간(점심시간)
                            self.count_down_start = False
                            self.remaining_time = 90 * self.min # 임시 시간
                            self.period += 1
                            self.show_classtime()

                        elif self.period == 9:
                            self.show_ending()

                        else:
                            self.count_down_start = False #요기도 바꿔야함
                            self.remaining_time = 60 * self.min
                            self.period += 1
                            self.show_classtime()


            self.draw()



tilemap = maps.world_1.stage_1
game = Game()
game.new(tilemap)

while game.running:
    game.main()

pygame.quit()
sys.exit()
pygame.mixer.music.stop()