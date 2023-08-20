import pygame
from config import*

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
	
setting_image = pygame.image.load("Image/설정.png").convert_alpha()
setting_button = Button(30, 60, setting_image, 0.02)

checklist_image = pygame.image.load("Image/파일.png").convert_alpha()
checklist_button = Button(100, 30, checklist_image, 1)

rightarrow_image = pygame.image.load('Image/우 화살표.png').convert_alpha()
rightarrow_button = Button(win_width() - 100, 800, rightarrow_image, 0.5)  # 위치와 크기 설정

leftarrow_image = pygame.image.load('Image/좌 화살표.png').convert_alpha()
leftarrow_button = Button(100, 800, leftarrow_image, 0.5)

couple1_image = pygame.image.load('Image/커플1.png').convert_alpha()
couple1_button = Button(100, 300, couple1_image, 0.1)

endgame_image = pygame.image.load('Image/endgame.png').convert_alpha()
endgame_button = Button(100, 300, endgame_image, 0.2)

menu_image = pygame.image.load('Image/아이콘.png').convert_alpha()
menu_button = Button(win_width() - 700, 10, menu_image, 0.5)

classtime_image = pygame.image.load('Image/수업 시간에 표시 할 것.png').convert_alpha()
classtime_button = Button(0, 0 , classtime_image, 0.5)