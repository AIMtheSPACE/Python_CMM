import pygame
import sys
from random import randint

#Reset pygame
pygame.init()

#pygame name
pygame.display.set_caption("러브캐처 인 청운")


# CLASS -----------------------------
# player setting
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ.png')
        
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

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
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

# camera setting
class Camera(pygame.sprite.Group):
    #여기 아래 배경 화면 삽입 코드
    def __init__(self):
        super().__init__()  # Fixed: added parentheses to call superclass constructor
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2  # Fixed: get_size() instead of get_sixe()
        self.half_h = self.display_surface.get_size()[1] // 2  # Fixed: get_size() instead of get_sixe()
        #/Users/joon/Desktop/Python Game Contest/Python_CMM/Image/ground.png
        # Ground
        self.ground_surf = pygame.image.load('/Users/joon/Desktop/Python Game Contest/Python_CMM/Image/ground.png').convert_alpha()
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

# Button setting
class Button():
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


# Screen
screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()

# settings -------------------------
camera_group = Camera()  # Fixed: create Camera object instead of pygame.sprite.Group()
player = Player((640, 360), camera_group)
show_settings_overlay = False

#이미지 불러오기
setting_image = pygame.image.load("/Users/joon/Desktop/Python Game Contest/설정.png").convert_alpha()
setting_button = Button(20, 20, setting_image, 0.01)  # 위치와 크기를 필요에 맞게 조절하세요

#첫 메인 화면 세팅
show_main_image = True  # New: Add a flag to control main image display

# 폰트 정의
font = pygame.font.SysFont("arialblack", 40)

# 색 정의
TEXT_COL = (0, 0, 0)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))

# 메인 코드 --------------------------------
while True:
    #게임 시작 끝내기와 스페이스로 시작
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_main_image = False  # Hide main image when spacebar is pressed
            elif event.key == pygame.K_p:
                show_settings_overlay = not show_settings_overlay 
    
    screen.fill('#71ddee')

    #첫 메인 화면
    if show_main_image:
        main_image = pygame.image.load('/Users/joon/Desktop/프레젠테이션1.jpg')
        main_image_rect = main_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(main_image, main_image_rect.topleft)
    else:
        camera_group.update()
        camera_group.custom_draw(player)
    
    #setting
    if setting_button.draw(screen) or (show_settings_overlay and event.type == pygame.KEYDOWN and event.key == pygame.K_p):
        show_settings_overlay = not show_settings_overlay

    if show_settings_overlay:
        overlay_color = (0, 0, 0, 128)
        overlay_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay_surface.fill(overlay_color)
        screen.blit(overlay_surface, (0, 0))

        # 첫 번째 상자 그리기
        box_color = (255, 255, 255)
        box_width = 200
        box_height = 100

        pygame.draw.rect(screen, box_color, (20, 100, box_width, box_height))
        draw_text("VOLUME", font, TEXT_COL, 20 + box_width // 2, 100 + box_height // 2)

        # 두 번째 상자 그리기
        pygame.draw.rect(screen, box_color, (240, 100, box_width, box_height))
        draw_text("CONTROL", font, TEXT_COL, 240 + box_width // 2, 100 + box_height // 2)

        # 세 번째 상자 그리기
        pygame.draw.rect(screen, box_color, (460, 100, box_width, box_height))
        draw_text("EXIT", font, TEXT_COL, 460 + box_width // 2, 100 + box_height // 2)
        

    pygame.display.update()
    clock.tick(60)
