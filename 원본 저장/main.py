import pygame, sys
from sounds import *
from player import *
from map_build import *
import maps
from sprites import *
from config import *
import pygame.mixer

pygame.init() # 초기화
pygame.display.set_caption("러브캐처 인 청운") # 화면 타이틀 이름
pygame.display.set_icon(pygame.image.load("Image/청운 로고.png") ) # 게임 아이콘 표시

class ChecklistImage(pygame.sprite.Sprite): # 체크리스트 이미지 보여주는 클래스
    def __init__(self, image_path, scale, center_position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale),
            int(self.image.get_height() * scale)
        ))
        self.rect = self.image.get_rect(center=center_position)


class Button(pygame.sprite.Sprite): # 게임 내의 전체적인 버튼들을 그릴 수 있게 해주는 버튼 클래스
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
        self.prev_mouse_state = False  # 이전의 마우스 상태 확인

        self.mainbutton = pygame.sprite.Group()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.is_mouse_over = True
            if pygame.mouse.get_pressed()[0] and not self.prev_mouse_state: # 왼쪽 마우스 클릭 확인하기
                self.callback()
                self.is_clicked = True
        else:
            self.is_mouse_over = False

        self.prev_mouse_state = pygame.mouse.get_pressed()[0]  # 마우스 상태를 원래대로 되돌리가


    def draw(self, surface):
        surface.blit(self.image, self.rect)


# 버튼그리려면 해야 할 것 아래 순서를 다 따라보고, 문제가 발생하면 단계 다시 확인해보기
# 1. init에 그룹 만들어주기 
# 2. new에 버튼 만들어주기
# 3. draw에 그룹 드로잉 해주기
# 4. 콜백에 쓴 글자와 같은 def콜백 함수 만들어 주기
# 5. event에서 업데이트 해주어야 함. 

class Game: # 메인 게임 실행 클래스
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True

        # 이미지 활용을 위한 설정
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
        self.couple_spritesheet = Spritesheet("Image/tile couple.png")

        # 그룹 생성하기
        self.setting_group = pygame.sprite.Group()
        self.classtime_group = pygame.sprite.Group()
        self.ending_group = pygame.sprite.Group() 
        self.checklist_group = pygame.sprite.Group()
        self.checklistimg_group = pygame.sprite.Group()
        self.mute_group = pygame.sprite.Group()

        # 폰트 초기 설정
        self.timer_font = pygame.font.SysFont("arialblack", 40) 
        self.couple_font = pygame.font.SysFont("arialblack", 15) # 필요에 따라 폰트 크기 조정하기

        # 값을 가지는 변수
        self.period = 1  # 초기 기간 값
        self.min = 1 # 테스르 하려면 이 값 줄여서 게임 빨리 진행 시키기
        self.page = 1
        self.stage = 1
        self.last_mute_toggle_time = 0 # 함수 명 바꾸자... 디파인 뮤트에 있음
        self.mute_toggle_delay = 100

        # True / False를 가지는 함수
        self.show_setting = False
        self.show_checklist = False
        self.show_checklist_img = False
        self.show_classtime_page = False
        self.show_vol = True
        self.count_down_start = True
        self.drawcountdown = True

        # 그 외의 초기 설정
        self.coupleOX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.tilemap = None
        self.remaining_time = 60 * self.min  # 기간을 초로 변환한 값
        self.last_time = pygame.time.get_ticks()  # last_time 속성 초기화
        self.mute_button = Button("Image/not mute.png", 100, 100, self.mute_callback, 2) # 세팅 누를 뺴마자 초기화 안 시키려고 뺌.

        # 음악 시작 하자 마자 실행 / 음악 관련 초기 설정
        pygame.mixer.init()  # Initialize mixer
        pygame.mixer.music.load("Song/배달의민족 - 배달은 자신있어.mp3")  # Load background music
        pygame.mixer.music.set_volume(0)  # Set music volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)
        self.button_click_sound = pygame.mixer.Sound("Song/Tiny Button Push Sound.mp3")
        self.class_start_sound = pygame.mixer.Sound("Song/41 시작종.mp3")
        self.class_end_sound = pygame.mixer.Sound("Song/42 종료종.mp3")

    def createTilemap(self, tilemap):
        self.all_sprites.empty()  # 기존 스프라이트 삭제
        self.desks.empty()  # 기존 책상 스프라이트 삭제
        self.walls.empty()  # 기존 벽 스프라이트 삭제
        self.closets.empty()  # 기존 신발장 스프라이트 삭제
        self.warp_up.empty()  # 기존 워프 스프라이트 삭제
        self.warp_down.empty()  # 기존 워프 스프라이트 삭제
        self.emptys.empty()
        self.hallways.empty()
        self.couples.empty()
        build_map(self, tilemap) # 맵 그리기

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
        self.couples = pygame.sprite.LayeredUpdates()
        self.tilemap = tilemap
        self.createTilemap(tilemap)

        # 버튼 생성
        self.button = Button("Image/설정.png", 10, 10, self.setting_callback, 1)
        self.setting_group.add(self.button)

    # 워프 시스템을 이용한 층간 이동 
    def change_tilemap_up(self): # 층 올라가기
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
    def change_tilemap_down(self): # 층 내려가기
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
        
    # 커플이 잡혔는지 확인
    def couplecaught(self):
        if self.stage == 1:
            self.coupleOX[0] = 1
        elif self.stage == 2:
            self.coupleOX[2] = 1
        elif self.stage == 3:
            self.coupleOX[4] = 1
        elif self.stage == 4:
            self.coupleOX[6] = 1
        elif self.stage == 5:
            self.coupleOX[8] = 1

    # 좌측 하단 세팅 버튼 눌렀을 떄 커플 관련 정보 표출
    def text_couple(self): 
        coupleleft_text = f"{self.coupleOX.count(0)} couple(s) left"
        coupleleft_surface = self.couple_font.render(coupleleft_text, True, (255, 235, 2))
        self.screen.blit(coupleleft_surface, (10, 450))  # 필요에 따라 위치 조정

        for index, value in enumerate(self.coupleOX):
            if value == 1:
                couplecaught_text = f"{index + 1} couple caught"
                couplecaught_surface = self.couple_font.render(couplecaught_text, True, (255, 235, 2))
                self.screen.blit(couplecaught_surface, (10, 500 + index*30))  # 필요에 따라 위치 조정
            elif value == 0:
                couplecaught_text = f"{index + 1} couple not caught"
                couplecaught_surface = self.couple_font.render(couplecaught_text, True, (25, 25, 2))
                self.screen.blit(couplecaught_surface, (10, 500 + index*30))  # 필요에 따라 위치 조정

    # 각종 이벤트
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.page = self.adjust_value(self.page, -1, 1, 10)
                    if self.show_checklist:
                        self.show_checklist_img = True
                elif event.key == pygame.K_RIGHT:
                    self.page = self.adjust_value(self.page, 1, 1, 10)
                    if self.show_checklist:
                        self.show_checklist_img = True
                elif event.key == pygame.K_UP:
                    if self.show_checklist:  # 이미 체크리스트가 표시 중일 때
                        self.checklistimg_group.empty()  # 이미지 삭제
                        self.show_checklist = False
                        self.show_checklist_img = False
                    else:
                        self.show_checklist = True
                        self.show_checklist_img = True
                elif event.key == pygame.K_SPACE:
                    if not self.count_down_start:
                        self.show_classtime_page = False
                        self.count_down_start = True
                        self.class_start_sound.play()
                        
                elif event.key == pygame.K_q: # 단축키 '큐' 세팅 열기
                    if not self.show_setting: 
                        # 새로운 버튼 생성
                        self.new_button = Button("Image/endgame.png", 100, 10, self.endgame_callback, 0.05)
                        self.setting_group.add(self.new_button)
                        
                        self.show_setting = True

                        self.checklist_button = Button("Image/checklist.png", 10, 100, self.checklist_callback, 2)
                        self.checklist_group.add(self.checklist_button)

                        self.mute_button = Button("Image/mute.png", 100, 100, self.mute_callback, 2)
                        self.mute_group.add(self.mute_button)
                    else:
                        # 버튼 숨기기
                        self.setting_group.remove(self.new_button)
                        self.checklist_group.remove(self.checklist_button)
                        self.mute_group.remove(self.mute_button)
                        self.show_setting = False

        # 업데이트
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

        if self.show_classtime_page:
            self.draw_scaled_image("Image/수업 시간에 표시 할 것.png", 1, (640, 450))

        if self.show_setting:
            rect_width = 175
            rect_height = 350
            rect_color = (230, 20, 232, 128) 
            pygame.draw.rect(self.screen, rect_color, (10, 450, rect_width, rect_height))

        # 픽셀로 그려진 커플 체크리스트 표시(잡혔는지 아닌지에 따라 다른 그림)
        if self.show_checklist_img:
            if self.page == 1:
                if self.coupleOX[0] == 1:
                    image_path = "Image/checklist_1.png"
                else:
                    image_path = "Image/checklist_1_not.png"
            elif self.page == 2:
                if self.coupleOX[1] == 1:
                    image_path = "Image/checklist_2.png"
                else:
                    image_path = "Image/checklist_2_not.png"
            elif self.page == 3:
                if self.coupleOX[2] == 1:
                    image_path = "Image/checklist_3.png"
                else:
                    image_path = "Image/checklist_3_not.png"
            elif self.page == 4:
                if self.coupleOX[3] == 1:
                    image_path = "Image/checklist_4.png"
                else:
                    image_path = "Image/checklist_4_not.png"
            elif self.page == 5:
                if self.coupleOX[4] == 1:
                    image_path = "Image/checklist_5.png"
                else:
                    image_path = "Image/checklist_5_not.png"
            elif self.page == 6:
                if self.coupleOX[5] == 1:
                    image_path = "Image/checklist_6.png"
                else:
                    image_path = "Image/checklist_6_not.png"
            elif self.page == 7:
                if self.coupleOX[6] == 1:
                    image_path = "Image/checklist_7.png"
                else:
                    image_path = "Image/checklist_7_not.png"
            elif self.page == 8:
                if self.coupleOX[7] == 1:
                    image_path = "Image/checklist_8.png"
                else:
                    image_path = "Image/checklist_8_not.png"
            elif self.page == 9:
                if self.coupleOX[8] == 1:
                    image_path = "Image/checklist_9.png"
                else:
                    image_path = "Image/checklist_9_not.png"
            elif self.page == 10:
                if self.coupleOX[9] == 1:
                    image_path = "Image/checklist_10.png"
                else:
                    image_path = "Image/checklist_10_not.png"
            
            image_center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            scaled_image = ChecklistImage(image_path, 1, image_center)
            self.checklistimg_group.empty()  # 기존 이미지 삭제
            self.checklistimg_group.add(scaled_image)  # 새로운 이미지 추가
            self.show_checklist_img = False

        # 그룹에 추가한 요소들 그리기
        self.setting_group.draw(self.screen)
        self.checklist_group.draw(self.screen)
        self.ending_group.draw(self.screen)
        self.checklistimg_group.draw(self.screen)
        self.mute_group.draw(self.screen)
        self.classtime_group.draw(self.screen)
        
        # 카운트 다운 타이머 표시
        if self.drawcountdown:
            rect_width = 1050
            rect_height = 50
            rect_color = (230, 20, 232, 8)  # Semi-transparent black color
            pygame.draw.rect(self.screen, rect_color, (190, 0, rect_width, rect_height))
            timer_text = f"{self.period} Period Break Time / Time left : {self.remaining_time // 60:02}:{self.remaining_time % 60:02}"
            timer_surface = self.timer_font.render(timer_text, True, (255, 235, 2))
            self.screen.blit(timer_surface, (400, -10))  # 필요에 따라 위치 조정

            floor_text = f"Floor {self.stage}"
            floor_surface = self.timer_font.render(floor_text, True, (255, 235, 2))
            self.screen.blit(floor_surface, (200, -10))  # 필요에 따라 위치 조정

        if self.show_setting: # 그냥 귀찮아서 원래 있던 함수 따라 씀. 세팅이 눌렸을 떄 실행
            self.text_couple()

        self.clock.tick(fps)
        pygame.display.update()

    # 세팅 버튼 눌렸을 때 실행
    def setting_callback(self): # 엔드 게임
        self.button_click_sound.play()

        if not self.show_setting:
            # 새로운 버튼 생성
            self.new_button = Button("Image/endgame.png", 100, 10, self.endgame_callback, 0.05)
            self.setting_group.add(self.new_button)
            
            self.show_setting = True

            self.checklist_button = Button("Image/checklist.png", 10, 100, self.checklist_callback, 2)
            self.checklist_group.add(self.checklist_button)

            self.mute_group.add(self.mute_button) # 다른 버튼 설정하는 부분은 init에 빼 두었음. 아니면 이미지가 자꾸 초기화 됨.

        else:
            # 버튼 숨기기
            self.setting_group.remove(self.new_button)
            self.checklist_group.remove(self.checklist_button)
            self.mute_group.remove(self.mute_button)
            self.show_setting = False

    # 체크리스트 버튼 눌렸을 때 실행
    def checklist_callback(self):
        self.button_click_sound.play()

        if self.show_checklist:  # 이미 체크리스트가 표시 중일 때
            self.checklistimg_group.empty()  # 이미지 삭제
            self.show_checklist = False
            self.show_checklist_img = False
        else:
            self.show_checklist = True
            self.show_checklist_img = True
            
    # 뮤트 버튼 눌렸을 떄 실행
    def mute_callback(self): # 요기 아래 코드 자세한 설명 필요!!
            current_time = pygame.time.get_ticks()
            if current_time - self.last_mute_toggle_time >= self.mute_toggle_delay:
                self.button_click_sound.play()
                self.show_vol = not self.show_vol
                pygame.mixer.music.set_volume(0.0 if self.show_vol else 0.5)
                self.last_mute_toggle_time = current_time

                # 뮤트 버튼 업데이트 하기
                mute_button_image = "Image/not mute.png" if self.show_vol else "Image/mute.png"
                self.mute_button = Button(mute_button_image, 100, 100, self.mute_callback, 2)
                self.mute_group.empty()
                self.mute_group.add(self.mute_button)
                
    # 엔스게임 콜백 이건 지금 작동 안할걸? 나중에 다시 확인해보고 삭제
    def endgame_callback(self): 
        self.button_click_sound.play()

        # 버튼을 누를 때 동작을 여기에!
        self.playing = False
        self.running = False

    # 수업 시간 표시 기능
    def show_classtime(self): 
        show_classtime_img = True
        while show_classtime_img:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        show_classtime_img = False
                        self.count_down_start = True
        
    def show_ending(self): # 엔딩 코드 여기다 !!!! 수정 필수 여기가 찐
        self.ending_button = Button("Image/endgame.png", 100, 100, self.endgame_callback, 0.5)
        self.ending_group.add(self.ending_button)
        if self.coupleOX.count(1) == 10:
            print("성공")
        else:
            print("실패")

    # 클래스 타임 화면에서 사라지고, 카운트 다운 시작
    def classtime_callback(self):
        self.class_start_sound.play()
        self.classtime_group.remove(self.classtime_button)
        self.count_down_start = True

    # 화살표로 변수 값 변경할때 리미트 주는거
    def adjust_value(self, value, change, min_value, max_value):
            new_value = value + change
            return max(min(new_value, max_value), min_value)

    # 스케일된 이미지 그리기 
    def draw_scaled_image(self, image, scale, center_position):
        self.image = pygame.image.load(image)  # 이미지 확장자 추가
        scaled_image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale),
            int(self.image.get_height() * scale)
        ))
        scaled_image_rect = scaled_image.get_rect(center=center_position)
        self.screen.blit(scaled_image, scaled_image_rect.topleft)

    # 시작 인트로 이미지 표시 기능(추가 원하면, 그 리스트 늘리면 됨 그리고 관련 수정 좀 하고)
    def show_intro_images(self):
        intro_images = ["Image/배경화면.png", "Image/조작법.png", "Image/대지 1.png"] # 첫번째 
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
    # 메인 실행 코드
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
                            self.show_classtime_page = True
                            self.class_end_sound.play()
                            

                        elif self.period == 9:
                            self.show_ending()
                            self.drawcountdown = False # 카운트 다운 표시 하지 않게 하기 위함

                        else:
                            self.count_down_start = False #요기도 바꿔야함
                            self.remaining_time = 60 * self.min
                            self.period += 1
                            self.show_classtime_page = True
                            self.class_end_sound.play()
                            
                            # 여기다 그릴 것
            self.draw()

tilemap = maps.world_1.stage_1
game = Game()
game.new(tilemap)

while game.running:
    game.main()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
