import pygame, sys
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
        self.image = pygame.image.load(image_path) # 이미지 불러오기, 아래 스케일 조절
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
        self.callback = callback # 콜백 사용 할 수 있는 기능을 추가함.
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

        self.prev_mouse_state = pygame.mouse.get_pressed()[0]  # 마우스 상태를 원래대로 되돌리기


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
        pygame.init() # 초기화 및 게임 초기 설정
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True

        # 이미지 활용을 위한 설정
        self.desk1_spritesheet = Spritesheet("Image/tile desk1.png")
        self.desk2_spritesheet = Spritesheet("Image/tile desk2.png")
        self.desk3_spritesheet = Spritesheet("Image/tile desk3.png")
        self.desk4_spritesheet = Spritesheet("Image/tile desk4.png")
        self.desk5_spritesheet = Spritesheet("Image/tile desk(1).png")
        self.desk6_spritesheet = Spritesheet("Image/tile desk(2).png")
        self.desk7_spritesheet = Spritesheet("Image/tile desk(3).png")
        self.desk8_spritesheet = Spritesheet("Image/tile desk(4).png")
        
        self.hallway_spritesheet = Spritesheet("Image/tile hallway.jpeg")
        self.closet_spritesheet = Spritesheet("Image/tile shoes closet.jpeg")
        self.wooden_spritesheet = Spritesheet("Image/tile wooden.jpeg")
        self.wall_spritesheet = Spritesheet("Image/tile wall.png")
        self.warp_up_spritesheet = Spritesheet("Image/tile up.jpeg")
        self.warp_down_spritesheet = Spritesheet("Image/tile down.jpeg")
        self.character_spritesheet = Spritesheet("Image/character.png")
        self.empty_spritesheet = Spritesheet("Image/tile black.png")
        self.stair_spritesheet = Spritesheet("Image/tile marble.png")
        self.white_spritesheet = Spritesheet("Image/tile white.png")
        
        self.couple1_w_spritesheet = Spritesheet("Image/tile couple1 (w).png")
        self.couple2_w_spritesheet = Spritesheet("Image/tile couple2 (w).png")
        self.couple3_w_spritesheet = Spritesheet("Image/tile couple3 (w).png")
        self.couple4_w_spritesheet = Spritesheet("Image/tile couple4 (w).png")
        self.couple5_w_spritesheet = Spritesheet("Image/tile couple5 (w).png")
        self.couple6_w_spritesheet = Spritesheet("Image/tile couple6 (w).png")
        self.couple7_w_spritesheet = Spritesheet("Image/tile couple7 (w).png")
        self.couple8_w_spritesheet = Spritesheet("Image/tile couple8 (w).png")
        self.couple9_w_spritesheet = Spritesheet("Image/tile couple9 (w).png")
        self.couple10_w_spritesheet = Spritesheet("Image/tile couple10 (w).png")

        self.couple1_spritesheet = Spritesheet("Image/tile couple1.png")
        self.couple2_spritesheet = Spritesheet("Image/tile couple2.png")
        self.couple3_spritesheet = Spritesheet("Image/tile couple3.png")
        self.couple4_spritesheet = Spritesheet("Image/tile couple4.png")
        self.couple5_spritesheet = Spritesheet("Image/tile couple5.png")
        self.couple6_spritesheet = Spritesheet("Image/tile couple6.png")
        self.couple7_spritesheet = Spritesheet("Image/tile couple7.png")
        self.couple8_spritesheet = Spritesheet("Image/tile couple8.png")
        self.couple9_spritesheet = Spritesheet("Image/tile couple9.png")
        self.couple10_spritesheet = Spritesheet("Image/tile couple10.png")
        
        self.student1_spritesheet = Spritesheet("Image/tile student1.png")
        self.student2_spritesheet = Spritesheet("Image/tile student2.png")
        self.student3_spritesheet = Spritesheet("Image/tile student3.png")
        self.student4_spritesheet = Spritesheet("Image/tile student4.png")
        self.student5_spritesheet = Spritesheet("Image/tile student5.png")
        self.student6_spritesheet = Spritesheet("Image/tile student6.png")

        self.student1_w_spritesheet = Spritesheet("Image/tile student1 (w).png")
        self.student2_w_spritesheet = Spritesheet("Image/tile student2 (w).png")
        self.student3_w_spritesheet = Spritesheet("Image/tile student3 (w).png")
        self.student4_w_spritesheet = Spritesheet("Image/tile student4 (w).png")
        self.student5_w_spritesheet = Spritesheet("Image/tile student5 (w).png")
        self.student6_w_spritesheet = Spritesheet("Image/tile student6 (w).png")
        
        self.umbrella1_spritesheet = Spritesheet("Image/tile umbrella1.png")
        self.umbrella2_spritesheet = Spritesheet("Image/tile umbrella2.png")
        self.umbrella3_spritesheet = Spritesheet("Image/tile umbrella3.png")
        self.umbrella4_spritesheet = Spritesheet("Image/tile umbrella4.png")
        self.umbrella5_spritesheet = Spritesheet("Image/tile umbrella5.png")
        self.umbrella6_spritesheet = Spritesheet("Image/tile umbrella6.png")

        # 그룹 생성하기
        self.setting_group = pygame.sprite.Group()
        self.ending_group = pygame.sprite.Group() 
        self.checklist_group = pygame.sprite.Group()
        self.checklistimg_group = pygame.sprite.Group()
        self.mute_group = pygame.sprite.Group()

        # 폰트 초기 설정
        self.timer_font = pygame.font.SysFont("Font/neodgm_code.ttf", 60)  # 타이머 용 폰트
        self.couple_font = pygame.font.SysFont("Font/neodgm_code.ttf", 25) # 커플 용 폰트

        # 값을 가지는 변수
        self.period = 1  # 초기 기간 값
        self.min = 1 # 테스르 하려면 이 값 줄여서 게임 빨리 진행 시키기
        self.page = 1
        self.stage = 2
        self.last_mute_toggle_time = 0 # 디파인 뮤트에 있음
        self.mute_toggle_delay = 100

        # True / False를 가지는 함수
        self.show_setting = False
        self.show_checklist = False
        self.show_checklist_img = False
        self.show_classtime_page = False
        self.show_vol = True
        self.count_down_start = True
        self.drawcountdown = True
        self.show_ending_stage = True
        self.show_fail_ending_stage = True

        # 그 외의 초기 설정
        self.coupleOX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.tilemap = None
        self.remaining_time = 60 * self.min  # 기간을 초로 변환한 값
        self.last_time = pygame.time.get_ticks()  # last_time 속성 초기화
        self.mute_button = Button("Image/mute.png", 100, 100, self.mute_callback, 2) # 세팅 누를 뺴마자 초기화 안 시키려고 뺌.

        # 음악 파일 불러오기
        pygame.mixer.init()
        self.button_click_sound = pygame.mixer.Sound("Song/Tiny Button Push Sound.mp3")
        self.class_start_sound = pygame.mixer.Sound("Song/41 시작종.mp3")
        self.class_end_sound = pygame.mixer.Sound("Song/42 종료종.mp3")
        self.couple_caught_sound = pygame.mixer.Sound("Song/Correct 9.mp3")
        self.intro_sound = pygame.mixer.Sound("Song/13-01 Back in my days.wav")
        self.main_sound = pygame.mixer.Sound("Song/13-03 Dinosaurs Are Still Alive.wav")


    def createTilemap(self, tilemap): # 타일맵 제작 코드
        self.all_sprites.empty()  # 기존 스프라이트 삭제
        self.woodens.empty() 
        self.desks.empty()  # 기존 책상 스프라이트 삭제
        self.walls.empty()  # 기존 벽 스프라이트 삭제
        self.closets.empty()  # 기존 신발장 스프라이트 삭제
        self.warp_up.empty()  # 기존 워프 스프라이트 삭제
        self.warp_down.empty()  # 기존 워프 스프라이트 삭제
        self.emptys.empty()
        self.white.empty()
        self.hallways.empty()
        self.couples.empty()
        self.stairs.empty()
        self.students.empty()
        self.umbrellas.empty() # 여러 기존 스프라이트 삭제

        # 맵의 시작 위치를 다르게
        if self.coupleOX.count(1) == 10 or self.period == 9:
            build_map_end(self,tilemap)
        else:
            build_map(self, tilemap) # 맵 그리기

    def new(self, tilemap):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.woodens = pygame.sprite.LayeredUpdates()
        self.desks = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        self.closets = pygame.sprite.LayeredUpdates()
        self.warp_up = pygame.sprite.LayeredUpdates()
        self.warp_down = pygame.sprite.LayeredUpdates()
        self.emptys = pygame.sprite.LayeredUpdates()
        self.white = pygame.sprite.LayeredUpdates()
        self.hallways = pygame.sprite.LayeredUpdates()
        self.couples = pygame.sprite.LayeredUpdates()
        self.stairs = pygame.sprite.LayeredUpdates()
        self.students = pygame.sprite.LayeredUpdates()
        self.umbrellas = pygame.sprite.LayeredUpdates()
        self.tilemap = tilemap
        self.createTilemap(tilemap)

        # 설정 버튼 생성
        self.button = Button("Image/설정.png", 10, 10, self.setting_callback, 1)
        self.setting_group.add(self.button)

    # 워프 시스템을 이용한 층간 이동 
    def change_tilemap_up(self): # 층 올라가기
        self.stage += 1
        a = 30
        b = 80
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
            self.tilemap = maps.worldW_1.stage_5
        
        self.createTilemap(self.tilemap)
    
    def go_back_to_office(self): # 쉬는 시간 끝나면 다시 교무실로
        self.stage = 2
        self.tilemap = maps.world_1.stage_2
        self.createTilemap(self.tilemap)


    # 성공 / 실패 엔딩 용
    def show_end_of_the_game(self): # 엔딩 조건을 먼족 시켰을 떄 가는 맵
        self.tilemap = maps.world_1.stage_ending_success
        self.createTilemap(self.tilemap)

    def show_end_of_the_game_fail(self): # 실패 엔딩
        self.tilemap = maps.world_1.stage_ending_fail
        self.createTilemap(self.tilemap)

       
    # 커플이 잡혔는지 확인
    def couplecaught(self, couple_num):
        if self.show_ending_stage and self.show_fail_ending_stage:
            if self.coupleOX[couple_num - 1] == 0: # 최초 1회만 소리가 나도록 설정
                self.couple_caught_sound.play()
                print(f"Couple {couple_num} was caught!")

            if couple_num == 1:
                self.coupleOX[0] = 1
            elif couple_num == 2:
                self.coupleOX[1] = 1
            elif couple_num == 3:
                self.coupleOX[2] = 1
            elif couple_num == 4:
                self.coupleOX[3] = 1
            elif couple_num == 5:
                self.coupleOX[4] = 1
            elif couple_num == 6:
                self.coupleOX[5] = 1
            elif couple_num == 7:
                self.coupleOX[6] = 1
            elif couple_num == 8:
                self.coupleOX[7] = 1
            elif couple_num == 9:
                self.coupleOX[8] = 1
            elif couple_num == 10:
                self.coupleOX[9] = 1

    # 좌측 하단 세팅 버튼 눌렀을 떄 커플 관련 정보 표출
    def text_couple(self): 
        coupleleft_text = f"{self.coupleOX.count(0)} couple(s) left"
        coupleleft_surface = self.couple_font.render(coupleleft_text, True, (255, 235, 2))
        self.screen.blit(coupleleft_surface, (20, 450))  # 필요에 따라 위치 조정

        for index, value in enumerate(self.coupleOX): # 반복적인 일을 처리하기 위함
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
                elif event.key == pygame.K_SPACE: # 여기 수정 함
                    if not self.count_down_start and self.show_ending_stage and self.show_fail_ending_stage:
                        self.show_classtime_page = False
                        self.count_down_start = True
                        self.class_start_sound.play() 
                        self.main_sound.play(fade_ms = 10000)
                        
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
        self.ending_group.update()
        self.checklist_group.update()
        self.checklistimg_group.update()
        self.mute_group.update()

    def update(self):
        self.all_sprites.update()

    def draw(self): # 화면에 그리는 기능을 담당
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)
        

        # 성공 엔딩 보여 줄때 출력 할 것
        if not self.show_ending_stage:
            ending_text = "Congratulations! You caught all!"
            ending_surface = self.timer_font.render(ending_text, True, (255, 235, 2), (0, 0, 0))
            self.screen.blit(ending_surface, (330, 500)) 

        # 실패 엔딩 보여 줄때 출력 할 것
        if not self.show_fail_ending_stage:
            ending_text = "You Failed."
            ending_surface = self.timer_font.render(ending_text, True, (255, 235, 2), (0, 0, 0))
            self.screen.blit(ending_surface, (518, 500)) 

        # 성공 / 실패 둘 중 하나의 엔딩을 보게 되면 False로 바뀌며 이게 다 실행되지 않음.
        if self.show_ending_stage and self.show_fail_ending_stage:
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
            self.mute_group.draw(self.screen) #@
           
            # 카운트 다운 타이머 표시
            if self.drawcountdown:
                rect_width = 1050
                rect_height = 50
                # 점심 시간 쉬는 시간 구분을 위해서
                if self.period == 4:
                    rect_color = (230, 20, 232)
                    timer_text = f"Lunch Time / Time left : {self.remaining_time // 60:02}:{self.remaining_time % 60:02}"
                    timer_surface = self.timer_font.render(timer_text, True, (255, 235, 2), rect_color)
                    self.screen.blit(timer_surface, (400, 0))  # 필요에 따라 위치 조정
                else:
                    rect_color = (230, 20, 232)
                    timer_text = f"{self.period} Period Break Time / Time left : {self.remaining_time // 60:02}:{self.remaining_time % 60:02}"
                    timer_surface = self.timer_font.render(timer_text, True, (255, 235, 2), rect_color)
                    self.screen.blit(timer_surface, (400, 0))  # 필요에 따라 위치 조정

                floor_text = f"Floor {self.stage}"
                floor_surface = self.timer_font.render(floor_text, True, (255, 235, 2), rect_color)
                self.screen.blit(floor_surface, (200, 0))  # 필요에 따라 위치 조정

            if self.show_setting: # 그냥 귀찮아서 원래 있던 함수 따라 씀. 세팅이 눌렸을 떄 실행
                self.text_couple()


            # 가장 위에 표시하기 위함
            if self.show_classtime_page:
                self.draw_scaled_image("Image/classtimeIMG.png", 0.25, (675, 485))


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
            
    # 뮤트 버튼 눌렸을 떄 실행 @
    def mute_callback(self):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_mute_toggle_time >= self.mute_toggle_delay:
                self.button_click_sound.play()
                self.show_vol = not self.show_vol
                if self.show_vol:
                    self.main_sound.play()
                else: 
                    self.main_sound.stop()
                self.last_mute_toggle_time = current_time

                # 뮤트 버튼 업데이트 하기
                mute_button_image = "Image/mute.png" if self.show_vol else "Image/not mute.png"
                self.mute_button = Button(mute_button_image, 100, 100, self.mute_callback, 2)
                self.mute_group.empty()
                self.mute_group.add(self.mute_button)
                
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

    # 화살표로 변수 값 변경할때 리미트 주는거
    def adjust_value(self, value, change, min_value, max_value):
            new_value = value + change
            return max(min(new_value, max_value), min_value)

    # 스케일된 이미지 그리기 많이 사용하려 하였으나 1회 만 사용함
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

        intro_images = ["Image/배경화면.png", "Image/조작법.png", "Image/info.png"] # 첫번째 
        current_intro_index = 0
        total_intro_images = len(intro_images)
        show_intro = True
        self.intro_sound.play()
        while show_intro:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.button_click_sound.play()
                        current_intro_index += 1
                        if current_intro_index >= total_intro_images:
                            show_intro = False
                            self.intro_sound.fadeout(2000) # 페이드 아웃
                            self.main_sound.play(loops = -1, fade_ms = 20000) # 페이드 인

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
            
            # 엔딩 볼 때 넘어가는 스테이지
            if self.coupleOX.count(1) == 10 and self.show_ending_stage:
                self.show_ending_stage = False
                self.show_end_of_the_game()
                
            if self.period == 9 and self.show_fail_ending_stage:
                self.show_fail_ending_stage = False
                self.show_end_of_the_game_fail()

            if self.show_fail_ending_stage and self.show_ending_stage:
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
                                self.main_sound.fadeout(1000)
                                self.class_end_sound.play()
                                self.go_back_to_office()
                                

                            elif self.period == 9:
                                self.drawcountdown = False # 카운트 다운 표시 하지 않게 하기 위함

                            else:
                                self.count_down_start = False
                                self.remaining_time = 60 * self.min
                                self.period += 1
                                self.show_classtime_page = True
                                self.main_sound.fadeout(1000)
                                self.class_end_sound.play()
                                self.go_back_to_office()
                                
                                # 여기다 그릴 것
                
            self.draw()

tilemap = maps.world_1.stage_2
game = Game()
game.new(tilemap)

while game.running:
    game.main()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()