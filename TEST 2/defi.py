import pygame
import sys
screen = pygame.display.set_mode((1280, 900)) 
clock = pygame.time.Clock()
pygame.init() # 초기화

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