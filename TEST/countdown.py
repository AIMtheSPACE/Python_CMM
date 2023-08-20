import pygame
import sys

pygame.init()

font = pygame.font.SysFont("arialblack", 40) # 폰트 설정
TEXT_COL = (0, 0, 0)
clock = pygame.time.Clock()
period = 1
screen = pygame.display.set_mode((1280,900))

def draw_text(text, font, text_col, x, y): # 글 쓰기
    img = font.render(text, True, text_col)
    screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))

def start_countdown(screen, period, countdown_duration):
    current_time = pygame.time.get_ticks() // 1000
    countdown_start_time = current_time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


        remaining_time = countdown_duration - (current_time - countdown_start_time)
        if remaining_time >= 0:
            if period == 4:
                countdown_text = f"Lunchtime/ time left : {remaining_time // 60:02}:{remaining_time % 60:02}"
            else:
                countdown_text = f"{period}period breaktime / time left :  {remaining_time // 60:02}:{remaining_time % 60:02}"
            draw_text(countdown_text, font, TEXT_COL, screen.get_width() // 2, screen.get_height() // 2)

            pygame.display.flip()  # 화면 업데이트
            clock.tick(1)  # 1 FPS로 제한

            if remaining_time == 0:
                period += 1
                return

            current_time = pygame.time.get_ticks() // 1000