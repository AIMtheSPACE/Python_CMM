import pygame
import sys
from random import randint
# --------------------------------- 여러 Class 설정 ---------------------------------
class Player(pygame.sprite.Sprite): # player setting
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('Image/ㅎㅇㅂ.png')
        
        #resizing
        original_size = self.image.get_size()
        new_width = 100
        new_height = int(original_size[1] * (new_width / original_size[0]))
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        new_position = self.rect.center + self.direction * self.speed

        # Check if the new position is within the background boundaries
        within_x_boundary = 0 <= new_position.x <= camera_group.ground_rect.width
        within_y_boundary = 0 <= new_position.y <= camera_group.ground_rect.height

        if within_x_boundary and within_y_boundary:
            self.rect.center = new_position

class Camera(pygame.sprite.Group): # camera setting
    #여기 아래 배경 화면 삽입 코드
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2  # Fixed: get_size() instead of get_sixe()
        self.half_h = self.display_surface.get_size()[1] // 2  # Fixed: get_size() instead of get_sixe()
        
        #/Users/joon/Desktop/Python Game Contest/Python_CMM/Image/ground.png
        # Ground
        self.ground_surf = pygame.image.load('Image/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h
        
        # Adjust camera offset to keep the character within the background boundaries
        self.offset.x = max(0, min(self.offset.x, self.ground_rect.width - self.display_surface.get_width()))
        self.offset.y = max(0, min(self.offset.y, self.ground_rect.height - self.display_surface.get_height()))

    def custom_draw(self, player):  # Fixed: typo, should be 'custom_draw' instead of 'center_terget_camera'
        self.center_target_camera(player)  # Fixed: typo, should be 'center_target_camera'

        # Ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)  # Fixed: use 'offset_pos' instead of 'sprite.rect'

class Button(): # Button setting
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

# --------------------------------- setting ---------------------------------
pygame.init() # 초기화
pygame.display.set_caption("러브캐처 인 청운") # 화면 이름
pygame.display.set_icon(pygame.image.load("Image/청운 로고.png") )
screen = pygame.display.set_mode((1280, 900)) 
clock = pygame.time.Clock()
camera_group = Camera()
player = Player((640, 360), camera_group)

# --------------------------------- 여러 함수 설정 ---------------------------------
def draw_text(text, font, text_col, x, y): # 글 쓰기
    img = font.render(text, True, text_col)
    screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))

def adjust_value(value, change, min_value, max_value): #함수 이름 바꿀 것. page 바꾸기
    new_value = value + change
    return max(min(new_value, max_value), min_value)

def draw_scaled_image(image, scale, center_position): # 이미지 스케일링
    scaled_image = pygame.transform.scale(image, (
        int(image.get_width() * scale),
        int(image.get_height() * scale)
    ))
    scaled_image_rect = scaled_image.get_rect(center=center_position)
    screen.blit(scaled_image, scaled_image_rect.topleft)

def draw_checklist_line_image(page, couple_index): # 첵크리스트 선 그리기
    images = [
        [],
        [page1_line_1_image, page1_line_2_image, page1_line_3_image],
        [page2_line_1_image, page2_line_2_image, page2_line_3_image],
        [page3_line_1_image, page3_line_2_image, page3_line_3_image],
        [page4_line_1_image, page4_line_2_image, page4_line_3_image]
    ]
    if 1 <= page <= 4:
        if 0 <= couple_index < len(images[page]):
            image = images[page][couple_index]
            draw_scaled_image(image, 0.3, (screen.get_width() // 2, screen.get_height() // 2))

def display_countdown(period, screen, remaining_time): # 카운트 다운 표시
    countdown_text = f"{period} Period Break Time / Time left : {remaining_time // 60:02}:{remaining_time % 60:02}"
    countdown_font = pygame.font.SysFont("arialblack", 20)
    countdown_surface = countdown_font.render(countdown_text, True, TEXT_COL)
    countdown_rect = countdown_surface.get_rect(topright=(screen.get_width() - 10, 10))
    screen.blit(countdown_surface, countdown_rect)

def draw_settings_overlay(screen, font): # 세팅 아이콘 버튼 함수(2곳에 넣어서)
    overlay_color = (0, 0, 0, 128)
    overlay_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay_surface.fill(overlay_color)
    screen.blit(overlay_surface, (0, 0))

    box_color = (255, 255, 255)
    box_width = 200
    box_height = 100

    pygame.draw.rect(screen, box_color, (20, 100, box_width, box_height))
    draw_text("VOLUME", font, TEXT_COL, 20 + box_width // 2, 100 + box_height // 2)

    pygame.draw.rect(screen, box_color, (240, 100, box_width, box_height))
    draw_text("CONTROL", font, TEXT_COL, 240 + box_width // 2, 100 + box_height // 2)

def draw_endgame_overlay(screen): # 위의 세팅과 같은 이유로 만든 세팅 안의 엔드게임 함수
    if endgame_button.draw(screen):
        pygame.quit()
        sys.exit()
        
# --------------------------------- 여러 이미지 초기에 불러오기 ---------------------------------
page1_line_1_image = pygame.image.load('Image/line.png').convert_alpha()
page1_line_2_image = pygame.image.load('Image/line.png').convert_alpha()
page1_line_3_image = pygame.image.load('Image/line.png').convert_alpha()

page2_line_1_image = pygame.image.load('Image/line.png').convert_alpha()
page2_line_2_image = pygame.image.load('Image/line.png').convert_alpha()
page2_line_3_image = pygame.image.load('Image/line.png').convert_alpha()

page3_line_1_image = pygame.image.load('Image/line.png').convert_alpha()
page3_line_2_image = pygame.image.load('Image/line.png').convert_alpha()
page3_line_3_image = pygame.image.load('Image/line.png').convert_alpha()

page4_line_1_image = pygame.image.load('Image/line.png').convert_alpha()
page4_line_2_image = pygame.image.load('Image/line.png').convert_alpha()
page4_line_3_image = pygame.image.load('Image/line.png').convert_alpha()


bigchecklist1_image = pygame.image.load('Image/첵리 1.png').convert_alpha()
bigchecklist2_image = pygame.image.load('Image/첵리 2.png').convert_alpha()
bigchecklist3_image = pygame.image.load('Image/첵리 3.png').convert_alpha()
bigchecklist4_image = pygame.image.load('Image/첵리 4.png').convert_alpha()

main_image = pygame.image.load('Image/배경화면.jpeg').convert_alpha()
# 누를 수 있는 버튼 세팅
setting_image = pygame.image.load("Image/설정.png").convert_alpha()
setting_button = Button(30, 60, setting_image, 0.02)

checklist_image = pygame.image.load("Image/파일.png").convert_alpha()
checklist_button = Button(100, 30, checklist_image, 1)

rightarrow_image = pygame.image.load('Image/우 화살표.png').convert_alpha()
rightarrow_button = Button(screen.get_width() - 100, 800, rightarrow_image, 0.5)  # 위치와 크기 설정

leftarrow_image = pygame.image.load('Image/좌 화살표.png').convert_alpha()
leftarrow_button = Button(100, 800, leftarrow_image, 0.5)

couple1_image = pygame.image.load('Image/커플1.png').convert_alpha()
couple1_button = Button(100, 300, couple1_image, 0.1)

endgame_image = pygame.image.load('Image/endgame.png').convert_alpha()
endgame_button = Button(100, 300, endgame_image, 0.2)

menu_image = pygame.image.load('Image/아이콘.png').convert_alpha()
menu_button = Button(screen.get_width() - 700, 10, menu_image, 0.5)

classtime_image = pygame.image.load('Image/수업 시간에 표시 할 것.png').convert_alpha()
classtime_button = Button(0, 0 , classtime_image, 0.5)

# --------------------------------- 화면 전환을 위한 설정 ---------------------------------
show_main_image = True
show_intro_image = False
show_settings_overlay = False
show_checklist_overlay = False
show_right_arrow = False
show_left_arrow = False

# --------------------------------- 초기값 ---------------------------------
period = 1
page = 1 #현재 페이지
current_image = "main"  # 현재 표시할 이미지를 나타내는 변수
countdown_start_time = None
countdown_duration = 10000# 쉬는 시간 시간 조절 기능(점심 시간은 # 점심 시간 조절 검색해서 바꿀 것))
font = pygame.font.SysFont("arialblack", 40) # 폰트 설정
TEXT_COL = (0, 0, 0)
page1couple = [0, 0, 0] # 4페이지, 페이지당 3커플
page2couple = [0, 0, 0]
page3couple = [0, 0, 0]
page4couple = [0, 0, 0]

# --------------------------------- 메인 이벤트 함수 ---------------------------------
while True:
    current_time = pygame.time.get_ticks() // 1000  # 현재 시간(초) 가져오기
    screen.fill('#71ddee')

    for event in pygame.event.get(): # 종류 및 키 값 받아오기 등
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_image == "main":
                    current_image = "intro"  # 이미지 변경

            elif event.key == pygame.K_p:
                show_settings_overlay = not show_settings_overlay

            elif event.key == pygame.K_l:
                show_checklist_overlay = not show_checklist_overlay
                show_right_arrow = not show_right_arrow
                show_left_arrow = not show_left_arrow

            elif event.key == pygame.K_SEMICOLON:
                page = adjust_value(page, 1, 1, 4)

            elif event.key == pygame.K_k:
                page = adjust_value(page, -1, 1, 4)

    if current_image == "main": # 메인 이미지 노출
        draw_scaled_image(main_image, 0.9, (screen.get_width() // 2, screen.get_height() // 2))
        

    elif current_image == "intro": # 인트로 이미지 노출
        intro_image = pygame.image.load('Image/intro.png').convert_alpha()
        intro_image_rect = intro_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(intro_image, intro_image_rect.topleft)
        
        # 스페이스바를 눌렀을 때 이미지 변경
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    show_settings_overlay = not show_settings_overlay

                elif event.key == pygame.K_SPACE:
                    current_image = "game"  # 이미지 변경
                    countdown_start_time = current_time  # 카운트다운 시작 시간 설정

            # 세팅 버튼 구현
        if setting_button.draw(screen) or (show_settings_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_p):
            show_settings_overlay = not show_settings_overlay

        if show_settings_overlay:
            draw_settings_overlay(screen, font)
            draw_endgame_overlay(screen)

    # 메인 게임 플레이 시
    elif current_image == "game":
        camera_group.update()
        camera_group.custom_draw(player)

        if setting_button.draw(screen) or (show_settings_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_p):
            show_settings_overlay = not show_settings_overlay

        if show_settings_overlay:
            draw_settings_overlay(screen, font)
            draw_endgame_overlay(screen)

        if menu_button.draw(screen): # 메뉴 임시 설정
            pygame.quit()
            sys.exit()

        # 체크리스트 띄우는 코드
        if checklist_button.draw(screen) or (show_checklist_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_l):
            # 체크리스트 노출
            show_checklist_overlay = not show_checklist_overlay
            # 화살표 노출
            show_right_arrow = not show_right_arrow
            show_left_arrow = not show_left_arrow

        if show_checklist_overlay:
            overlay_color = (0, 0, 0, 128)
            overlay_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay_surface.fill(overlay_color)
            screen.blit(overlay_surface, (0, 0))

            # 선 표시
            if page == 1:
                draw_scaled_image(bigchecklist1_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
            elif page == 2:
                draw_scaled_image(bigchecklist2_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
            elif page ==3:
                draw_scaled_image(bigchecklist3_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
            elif page ==4:
                draw_scaled_image(bigchecklist4_image, 0.5, (screen.get_width() // 2, screen.get_height() // 2))
        
        if show_right_arrow and rightarrow_button.draw(screen):
            page = adjust_value(page, 1, 1, 5)

        if show_left_arrow and leftarrow_button.draw(screen):
            page = adjust_value(page, -1, 1, 5)

        #잘 카운트 되는지 알아보기 위한 코드 나중에 삭제
        draw_text(str(page), font, TEXT_COL, screen.get_width() - 50, screen.get_height() - 50)

        # 카운트 다운 시작
        if countdown_start_time is not None:
            remaining_time = countdown_duration - (current_time - countdown_start_time)
            if remaining_time > 0:
                if period == 4:
                    countdown_text = f"Lunch Time / Time left : {remaining_time // 60:02}:{remaining_time % 60:02}"
                    countdown_font = pygame.font.SysFont("arialblack", 20)
                    countdown_surface = countdown_font.render(countdown_text, True, TEXT_COL)
                    countdown_rect = countdown_surface.get_rect(topright=(screen.get_width() - 10, 10))
                    screen.blit(countdown_surface, countdown_rect)
                else:
                    display_countdown(period, screen, remaining_time)

            # 게임 끝 엔딩 화면으로 전환 -> 다른 곳으로 전환 되도록 바꿀 것
            if remaining_time == 0:
                current_image = "classtime" 
                period += 1

        # 커플 버튼 값 변경
        if couple1_button.draw(screen):
            page1couple[0] = 1

        # [커플코드] 체크 리스트 선 show or not (앞에서 누르면 함수값 1로 바꾸어 주는 거 필요)
        if show_checklist_overlay:
            for page_index, couple_list in enumerate([page1couple, page2couple, page3couple, page4couple], start=1):
                if page == page_index:
                    for couple_index, couple_value in enumerate(couple_list):
                        if couple_value == 1:
                            draw_checklist_line_image(page, couple_index)
        
    elif current_image == "end": # 게임 엔딩 화면
        end_image = pygame.image.load('Image/ending.png').convert_alpha()
        end_image_rect = end_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(end_image, end_image_rect.topleft)
    
    

    # 쉬는 시간 설정
    if current_image == "classtime":
        if classtime_button.draw(screen):
            current_image = "game"
            if period == 4:
                countdown_start_time = current_time + 10 # 점심 시간 조절
            elif period == 7:
                current_image = "end"
            else:
                countdown_start_time = current_time
       
    pygame.display.update()
    clock.tick(60)
